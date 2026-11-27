# Workstream R13 — running notes (kept from the first minute; clock = `date -u`)

Agent: independent review workstream R13. Brief: docs/science/workstreams/R13_brief.md.
Write area: experiments/science/ws_R13/ and docs/science/workstreams/R13_REPORT.md only.
Export under review (read-only): /tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_63e36f7/  (called <EXP>)

Kinds of checking used below: REVIEW (re-derived on paper) / REPLICATION (own code written from statements
before opening their scripts) / RE-RUN (their code) / READ ONLY.

## Log

- 2026-11-26 04:45:46 UTC  Start. Read R13_brief.md in full (108 lines). Created experiments/science/ws_R13/ and this file.
- 04:46:02  Read COMMON.md (115 lines), <EXP>/docs/collaboration/responses/theory/THY-RES-0011.md (289 lines, in full),
  <EXP>/docs/collaboration/messages/theory/THY-MSG-0015.md (56 lines, in full).
  Plan for item 1 (order matters for the independence of the replication): (1) read Thm 11.53 + remark in
  <EXP>/docs/THEORY_REPORT.md; (2) read HintRecursion.lean statements; (3) write my own cube recursion
  from the theorem's statement BEFORE opening t4_rate.py; (4) only then open t4_rate.py (docstring = proof).
- 04:50:55  Item 1, step (1)-(2) done (READ): <EXP>/docs/THEORY_REPORT.md lines 4290-4390 (setting, Thm 11.51, bracket
  procedures, Thm 11.52 statement with (11.18.2) and the definition of R[T]) and 4508-4603 (Thm 11.53 (a)-(d), proof of (c),
  the Remark "a rate for the recursion").  <EXP>/proofs/Frontiers/HintRecursion.lean lines 1-180 and 300-569 (StepLE, HintPair,
  StepLE.of_limit / of_macro / at_hint_fraction, step_from_hint_le, iterates_lt_hint_add, klBin_shift, gaussPair);
  CubeHintPair.lean declaration list + cubePair (lines 519-545, 619-640); BoundedAccuracy.lean lines 1-240
  (admissible, Rstep, exactRec, stepLE_exact, Rstep_anti, exactRec_props, exactRec_ge_hint, exactRec_tendsto_hint).
  NOT yet opened: experiments/coordinator_checks/nested_review_R6/ (any file).

  What the Lean statements give (my reading; hypotheses in full):
  * StepLE θna T T' := ∀ g φ β B, 0<β → β<g → 0<φ → φ<1 →
        (∀ γ ≥ β, min γ (φ·θna((g−β)/φ)) + (1−φ)·T(γ/(1−φ)) ≤ B) → T' g ≤ B.      ["T' ≤ R[T]" without suprema]
  * HintPair θna θh a h E: 0<h; 0<a; θna x ≤ a (x>0); θna continuous at every x>0; θna h = h;
        θna(e+θh e)=θh e, 0<θh e (0<e<E); e+θh e nondecreasing on (0,E) [stated for 0<e≤e'<E];
        ∃ L, h − L e ≤ θh e on (0,E).   NOT in the structure: a>h; θna nonincreasing; θna ≥ 0; L = 1; θh(0+)=h.
  * StepLE.of_limit (no HintPair needed): StepLE θna T T', T antitone on (0,∞) [∀x y, 0<x→x≤y→T y≤T x], 0<g, 0<φ<1,
        θna ContinuousAt (g/φ), 0 < φ·θna(g/φ), (∀γ, 0<γ≤φ·θna(g/φ) → γ+(1−φ)T(γ/(1−φ)) ≤ B)  ⊢  T' g ≤ B.
  * StepLE.of_macro: HintPair, StepLE, T antitone on (0,∞), 0<g, 0<φ<1, (∀γ, 0<γ≤φ·a → γ+(1−φ)T(γ/(1−φ)) ≤ B) ⊢ T' g ≤ B.
  * StepLE.at_hint_fraction: HintPair, StepLE, T antitone on (0,∞), 0<x<E, (∀y, 0<y≤x → y+T y ≤ C) ⊢ T' x ≤ θh x/(x+θh x)·C.
  * cubePair (u>0): HintPair (cubeNa u) (cubeHint u) (cubeA u) (cubeH u) (cubeEstar u); hint_lower proved with L = 1
        (inside the proof term, from cubeHint_add_mono at e=0 and cubeHint_zero; L=1 is not exposed by the structure, it IS
        available as cubeHint_add_mono + cubeHint_zero).
  * exactRec θna k = T_{k+1} of the report (index shift). stepLE_exact: θna ≥ 0, T ≥ 0 on (0,∞) ⊢ StepLE θna T (min(T, Rstep θna T)).
    exactRec_props: θna ≥0, antitone, ≤ C on (0,∞) ⊢ each exactRec k is ≥0, ≤C, antitone on (0,∞).
    exactRec_ge_hint (cube): cubeHintClip u g ≤ exactRec (cubeNa u) k g for all g>0  (so T_k ≥ θ_hint: the sign fact m_k ≥ 0).
  First paper pass over the Remark (before seeing their proof): Step I, the epoch map d ↦ d(Ja+h)/(Ja−hd), κ, c₁, c₂, limsup ≤ a,
  Step II with A(g) all re-derived by me and found consistent; details to be written in the report after reading the docstring.
  Things I will look for in their proof: (1) hanti (T_k antitone) supplied? (2) a>h assumed? (3) L=1 stated as a hypothesis of (b)?
  (4) the sign of m_k in "(1 − y/s)·m_k" (needs m_k ≥ 0, i.e. exactRec_ge_hint, or a case split).
- 04:54:02  Wrote r13_01_cube_recursion.py (OWN implementation of T_1 = theta_na, T_{k+1} = min(T_k, R[T_k]) on the cube; one-sided:
  a nonincreasing step function Uhat_k >= T_k, B_k >= sup T_k; see its docstring for the six reasons). Written from the
  statements of Thm 11.52/11.53 only; nothing in <EXP>/experiments/coordinator_checks/nested_review_R6/ opened so far.
  First test (u=1, 8 levels, grid ratio 1.05, 3 s): constants a=0.110944071672 h=0.029139138502 kappa=0.042648110203
  c1=0.712384852395 c2=6.352133391184 (their c1=0.712, c2=6.35, kappa=0.0427: agree). Bound (a) holds at k=1..8,
  max ratio 0.844 at k=1 (which is (a-h)/(c1/(1+c2)) - exact). Self-check "one step from theta_hint stays >= theta_hint": ok.
- 04:54:40  Production runs started in background (r13_02_run_cube.sh: u = 0.5, 1, 2; 60 levels; grid ratio 1.01, then 1.003; one process).
  sha256 of r13_01_cube_recursion.py at this moment (BEFORE opening their t4_rate.py): 89bc729bb0161360cb6650bc2bc4dfa7ffdfbb4f7e6f3ccce467fbe501153620
  Now opening <EXP>/experiments/coordinator_checks/nested_review_R6/ for the first time (README, t4_rate.py docstring = the proof).
- 04:59:53  Read <EXP>/experiments/coordinator_checks/nested_review_R6/t4_rate.py in full (242 lines; docstring = STATEMENT + PROOF;
  code = their one-sided iteration, G=160 grid points g_i = eps*(i/G)^1.5, 101 phi x 16 beta per point).
  REVIEW of the proof (line by line, on paper; details go to the report section 2):
  * (L1) = StepLE.of_limit at phi = g/h: side conditions 0<g, 0<g/h<1 (needs g<h), ContinuousAt theta_na (g/(g/h)) = at h
    (na_cont, h>0), 0 < (g/h)*theta_na(h) = g (na_h): all supplied.  WITHIN HYPOTHESES.  (The instantiation is not a named Lean
    lemma; it is done inline for T = T' in superSolution_le_hint lines 226-234.)
  * (L2) = StepLE.of_macro verbatim.  (L3) = StepLE.at_hint_fraction verbatim (needs 0<x<E).  hanti (T_k antitone on (0,inf)) is a
    hypothesis of the STATEMENT and for exactRec is exactRec_props.  WITHIN HYPOTHESES.
  * Lemma 1: correct (g < x0 h/(h+x0) <=> g h/(h-g) < x0; uses sigma <= 1 and gamma <= g).  Lemma 2: correct
    (phi a/(1-phi) < x0 <=> phi < x0/(a+x0); limit phi -> x0/(a+x0) is legitimate: a limit of upper bounds).
  * Epoch: J = ceil(1/c) = ceil(d) >= 1; slopes before the j-th application (j-1)c <= (J-1)c < 1: ok; ranges h/j: ok;
    T_{k+J+1} <= B J a/(J a + h); d' = d (J a + h)/(J a - h d), J a - h d >= d(a-h) > 0 (uses a > h): ok.
  * Closed form: d'-d = d h (1+d)/(J a - h d) > (d+2) h f(d) > (J+1) h f(d), f(d) = d(1+d)/((d(a-h)+a)(d+2)) increasing (both
    factors d/(d+2), (1+d)/(d(a-h)+a) increasing; the second because a-(a-h) = h > 0); kappa = h f(d_0) = h^2 a/((a-h)(a+h)(2a-h)): ok.
    d_m >= d_0 + kappa (k_m - 1); k <= k_m + J_m < k_m + d_m + 1 => d_m (1+kappa) > d_0 + kappa (k-2) => B_k - h <= c1/(k+c2),
    c2 = d_0/kappa - 2 = (a+h)(2a-h)/(ha) - 2, and k + c2 > 0 for k >= 1 because kappa < d_0.  ok.
    limsup: gain per level >= lambda' for any lambda' < h/(a-h) eventually => limsup k (B_k - h) <= h (1+lambda)/lambda = a.  ok.
  * (b): re-derived with general L: crossing value m (eps + L s)/(m + L s): ok; induction <=> c1 + L s <= A: ok; base m_1 <= a-h+Lg: ok.
    The positive part in m_k handles the sign (report's remark has no positive part; on the cube exactRec_ge_hint gives m_k >= 0).
  FINDINGS SO FAR on item 1: NO error in the mathematics.  Minor points:
   (m-a) report: "the gain per level increases with d" is true of the lower bound h f(d), not of the gain itself (sawtooth in d
         because of the ceiling: it reaches h/(a-h) at integer d from below and drops just above);
   (m-b) the displayed intermediate recursion of (b) is false in the degenerate case B_{k+1} < h - L s, m_k > 0 (abstract sequences
         only, e.g. T_2 = 0 with the Gaussian pair L = 1/2): there m_{k+1} = 0 > max{...}.  Fix: (.)_+ on the right or "max{0, ...}".
         The final bound is unaffected.  Also the "max{B_{k+1}-h, .}" is not needed: the crossing value alone bounds min of the two lines.
   (m-c) report: "uses only the three inequalities" - it also uses T_{k+1} <= T_k, T_k nonincreasing in x, T_1 <= a, a > h,
         hint_mono, L = 1 and T_k >= theta_hint (the last for the version without positive part).  All true for exactRec on the cube.
   (m-d) "at most A(g)/eta levels": k = ceil(A(g)/eta) suffices (rounding).
   (m-e) two objects called tau_k: sup T_k (remark after 11.53) and the bounded-accuracy sequence of sec. 11.19 remark (1)
         (tau_1 = a, tau_{k+1} = inf_phi sup_{gamma>=0}[...] with T_k(0) = tau_k).  By of_macro sup T_{k+1} <= tau_{k+1}(11.19);
         equality is numerical there ("max_g(T_k - theta_hint) = tau_k - h [N]").  The epoch argument also covers the 11.19
         sequence (same constants) - to be written in the report as an offered extension.
- 04:59:53  First production results (grid ratio 1.01, 60 levels, logs complete with END line for u=0.5 and u=1.0):
  bound (a) holds at all 60 levels, largest ratio (B_k-h)/(c1/(k+c2)) = 0.851 (u=0.5), 0.844 (u=1) at k=1 [= exact (a-h)(1+c2)/c1],
  then 0.318 / 0.310 at k=2 and < 0.02 from k=10; (b) holds at every grid point; the over-estimate never dips below theta_hint.
  My (B_k-h)k^2/a: 0.95 (k=2), 0.66-0.70 (k=5..10), then grows (stall of the one-sided mode: 1.7 at k=40, 3.1 at k=60).
- 05:03:15  r13_03_closed_form.py run (10 s; out/closed_form.log, complete with END): (A) constants at 40 digits
  u=0.5: a=0.0302998619808 h=0.00767286647803 kappa=0.039226642 c1=0.20327632 c2=6.6446939
  u=1:   a=0.110944071672  h=0.0291391385016  kappa=0.04264811  c1=0.71238485 c2=6.3521334 (c1/a=6.42112)
  u=2:   a=0.327813325473  h=0.0972809077466  kappa=0.056697173 c1=1.8130791  c2=5.4427633
  (B) exact rational test closed form vs epoch recursion, 11 pairs (a,h), k to 1e7: all three claims hold in every epoch;
  worst ratio (h/d_m)/(c1/(k+c2)) = 0.959 (cube u=1, k=2), sup over pairs -> 1 as h/a -> 0 or 1 (0.99995 at h/a=0.01, 0.999001 at 0.999).
  (C) 4016 pairs in floating point to k=1e9: 0 violations; k(B_k-h)/a at the last level of the last epoch in [1.000000, 1.000276].
- 05:03:15  RE-RUN of their t4_rate.py: byte-identical copy (sha256 1c6469353fb2...5629) placed in ws_R13/thy_copy_nested_R6/code/ so that its
  output goes to ws_R13/thy_copy_nested_R6/out/ (the script would otherwise write next to itself, i.e. into the export).
  python3 -I -B, 40 levels, 108 s, exit 0, "all checks passed: True"; output identical to their stored out_t4_rate.txt except the timing line.
- 05:15:06  tau_2 in closed form (r13_04_tau2.py, mpmath; out/tau2.log): tau_2/a = 0.5000267 (u=0.5), 0.5004100 (u=1), 0.5056154 (u=2).
  My one-sided B_2/a at u=1: 0.5009 (ratio 1.01), theirs (t4_rate.py) 0.5009; report sec. 11.19 remark (1) prints "0.5006" (K_REPORT's grid
  value; K_REPORT itself gives the closed form 0.5004a) and "h/a = 0.2627" (h/a = 0.2626471 -> 0.2626).  Minor, 4th decimal.
- 05:15:06  ITEM 2, sec. 11.32.  Read SCI-REV-0010 in full (267 lines), R10_REPORT.md sections 2, 3.4, 3.5, 5 (lines 84-199, 255-380, 414-473),
  <EXP> THEORY_REPORT.md 10090-10349 (sec. 11.32: Thm 11.116, Prop 11.117, "What the result is"), <EXP> docs/workstreams/Y_REPORT.md 1-75 (errata block).
  REPLICATION (own code r13_05_blocks_recursion.py, written from Thm 11.116(d) and the Setting; vertices by spanning trees; capacity by
  Blahut-Arimoto with dual bound; log out/blocks_recursion.log complete, 233 s):
   controls: u*(u=1) = 1.2183, 1.5261, 1.9807, 2.7497 (report 1.218, 1.526, 1.981, 2.750); p=1/2 gives the cube for L=1 and L=3 (38 vertices).
   L=3: a_inf <= 0.495806 at (0.3,3) [cube 0.502282, 0.9871], 0.467509 at (0.2,3) [0.9308], 0.509682 at (0.1,4) [0.8452]; 96 vertices each:
        their four digits and ours reproduced by a fourth code.  h at (0.1,4): my bracket at the grid maximum [0.2275, 0.2327] < cube 0.239250.
   L=1 ("blocks of one site", THEIR ADDITION): a-bound/cube and h-bound/cube > 1 in all 24 cells p in {0.3,0.2,0.1} x u in {1,1.5,2,2.5,3,4,5,6};
        smallest ratios 1.0099 (a, (0.3,6)) and 1.0753 (h, (0.3,6)).  Their sentence REPLICATED.
   L=2 (not in their text): the reversal of a shows already at (0.2,3) 0.979, (0.1,4) 0.885, (0.1,6) 0.931, not at (0.3,3) 1.020;
        h at (0.1,4): 0.998, (0.1,6): 0.960.
  FINDINGS sec. 11.32:
   (M) Prop 11.117(b) drops the hypothesis "d_0 symmetric" of our R10.1 (our report line 267-268, message sec. 4) while the Setting of sec. 11.32
       allows non-symmetric envelopes.  As worded it is FALSE: two points, d_0(0,1)=1, d_0(1,0)=0: F*(t)/((t(1-t)/2)u^2 V) -> 1/4
       (r13_06_small_slope_asym.py, certified brackets; out/small_slope_asym.log).  Their own proof sketch ("the two labels +-u f*") needs symmetry.
   (m) errata (e4) of Y_REPORT.md: "'multiplied by (1-p)/p' is a theorem at second order for finite chains" - at fixed n the theorem gives
       Var(sum s_i)/n (1.792 at n=4, p=0.3), (1-p)/p = 2.333 is the limit, proved from above only.  In sec. 11.32(b) the distinction IS kept
       in the sentence after "Hence ...", but the "Hence" sentence states the limit factor for "the three exponents" flatly.
   (m) (c): "E_F > ln cosh(u/2) (p != 1/2)" is false for p > 1/2 (E_F(0.7, u=1) = 0.0540 < 0.1201); true for p < 1/2; for p > 1/2 use 1-p (gauge).
   (m) errata (e5): "h >= 0.0300 at p = 0.02": our number is 0.029973 (rounded the wrong way for a lower bound).
   (m) table (a), p=0.1: a <= 0.1730 is R11's 0.172914; ours is 0.172043 ("yours and R11's, which agree" - to two digits); valid, not sharpest.
   (m) "What the result is": "lowers two of the three exponents where it is strong" without the cells: proved for a at p <= 0.3 and for h at
       p <= 0.2 only; at p = 0.4, 0.45 nothing is lowered at any computed slope; THY-RES-0011 sec. 8 last row "at u >= 3" over-states h (u = 4, 6 only).
   (ok) reversal cells, "between about u = 1.5 and those cells open", threshold bracket [0.4017, 0.4037] at p=0.1 (outward rounding of ours),
        m1, m2, m3, m4, m6, m7, m8, m9, m10: all present and correct; antiferromagnetic example 0.43 vs 1.23 on three sites re-derived by hand.
- 05:20:48  Cube production runs finished (all six logs end with "# END"; out/cube_runs.done).  Grid ratio 1.003 (N ~ 6150 points), 60 levels:
  u=0.5/1/2: bound (a) holds at all 60 levels; largest ratio 0.851/0.844/0.819 at k=1, 0.318/0.310/0.282 at k=2, < 0.006 from k=24.
  (b) holds at every grid point and level (largest ratio 0.820/0.811/0.777 at k=1).  Upper bounds never below theta_hint.
  B_k/a at u=1 (ratio 1.003): k=2 0.5008 (exact 0.50041), k=3 0.3621, k=4 0.3112, k=5 0.2902, k=6 0.2805, k=40 0.26326, k=60 0.26304 (h/a = 0.26265);
  K_REPORT's values 0.5006, 0.3613, 0.3108, 0.2898, 0.2803, ..., 0.2631 (k=40) are all slightly BELOW my upper bounds, as they must be if they are estimates of T_k(0+).
  (B_k-h)k^2/a (ratio 1.003): 0.95, 0.90, 0.78, 0.69, 0.64, 0.63 (k=8), 0.64 (10), 0.68 (16), 0.71 (20), 0.85 (32), 0.98 (40), 1.40 (60) - my over-estimate
  stalls later than theirs; "about 0.65/k^2" is consistent for k = 6..16 and not contradicted beyond (upper bounds only).
- 05:20:48  ITEM 3 (part): diff of imports.  HintRecursion/CubeHintPair/BoundedAccuracy.lean: IDENTICAL in our tree (so the three lemmas of item 1 are the
  ones compiled in our .lake build).  SoftMinLowerBound.lean: imports Mathlib + proofs.Frontiers.GeneralisedDips; all 12 transitive project imports
  IDENTICAL in our tree and built -> copy compiled: lean/SoftMinLowerBound_copy.lean (their file, sha256 0bbef45e..., + 5 appended lines
  #print axioms / #check), `lake env lean`, exit 0, 8 s, axioms [propext, Classical.choice, Quot.sound] for all four theorems
  (out/lean_SoftMinLowerBound_copy.log).  StateShares.lean: imports proofs.Frontiers.ShareCertificates - ABSENT in our tree -> NOT compiled (read only).
  BoxBennett.lean: imports BoxClass (absent) and BennettTwoPoint (absent under proofs/) -> NOT compiled (read only).
- 05:20:48  ITEM 2, share certificates.  Read SCI-REV-0012 in full (295 lines); P4_REPORT.md lines 340-410; <EXP> THEORY_REPORT.md 2218-2480
  (Thm 11.18a, Props 11.18b (a)-(e), 11.18c (a)-(c)); <EXP> proofs/Frontiers/StateShares.lean in full (296 lines).
  Lean vs wording: secondOrder_certified_of_state_shares = report (e) (no additivity hypothesis; cover with T_ik + T_ki; load with the excitation
  energy of M.energy + g; nonnegativity asked for all states incl. the reference - harmless); secondOrder_certified_of_deficit_shares = (d)
  (w only has to dominate the deficits; no positive part needed); energy_sub_eq_excitations_add_secondDiff = the identity for the known part;
  stateShare_witness: the negative half does not even assume s >= 0.  No hypothesis missing.
  BRUTE FORCE (own code r13_07_shares_bruteforce.py; out/shares_bruteforce.log, complete):
   (I) integrality gap (3 binary sites, A=(1,1,1), c12=c13=2, T23=10; c23 = 0 or 2): L-L(x0) = 0,1,1,1,0,0,12(10),9(7): x0 minimises (ties at {1,2},{1,3});
       relaxation value -1/2 (HiGHS; exact on a 1/20 grid of the reduced problem) at the point of the text; no state shares (4 > 3);
       no joint distribution has those marginals.  CONFIRMED.
   (II) Lean witness: shares (1/2, 5/2) valid; deficit 3 at (1,2),(2,1),(2,2) > Delta1+Delta2 = 2.  CONFIRMED.
   (III) 11.18c(a) counter-example (ours): 5 of 9 rectangles inside D; least member -3 at the three inner points; 8, 8, 17.  CONFIRMED.
   (IV) 400 random instances (2-4 sites, 2-3 states): "state shares exist <=> relaxation solved by x0" in 395 of 395 decided; 3 integrality gaps.
  FINDINGS: applied correctly.  One slip that is OURS: SCI-REV-0012 sec. 3 "with one or two of them changed neither form is the envelope" - with ONE
  changed site the pair form charges nothing, like the envelope (P4_REPORT 2.3(c)(i) has it right); their Thm 11.18a(c) repeats it ("with one or two
  of them changed neither does") right after its own correct "nothing in the pair form".
- 05:25:52  ITEM 2, Proposition 11.69b as replaced.  Read SCI-REV-0011 in full (186 lines), SCI-REV-0009 header + lines 100-145, R9_REPORT.md 451-690
  (sec. 4: definitions, Theorem R9.1 (a)-(g), proofs, checks, 4.5), R9_ADDENDUM.md 60-100, 186-200; <EXP> THEORY_REPORT.md 5972-6200 (Prop 11.69a end,
  Prop 11.69b (a)-(e), (f), (g), elementary estimate, proof, Verification); their r9/README.md + out_their_certificate_check.txt.
  (a)-(e): statement by statement identical to R9.1(a)-(e) (plus: admissible bonds of the concatenation; 0 in S_M for M >= 6; attainment "by none with fewer";
  their own unimodular set).  (f), (g): "read by us, the lemma re-derived, nothing computed" - status kept as ours [P], read only.  7.5 and 5 both quoted.
  Arithmetic re-done exactly (r13_08_r9_arith.py; out/r9_arith.log): det = 1 for our five vectors, for their five (4,5,7,8,10 beads) and for the five of
  SCI-REV-0011 sec. 4; norms 44, 16, 60; 108 = 15+54+36+3; projections generate Z^4 (gcd of 4x4 minors 1).
  THEIR THREE DISAGREEMENTS, checked in our files and in their history (read-only `git show <commit>:path`; their commits are in our object store):
   (1) G27 mutation history: RIGHT.  experiments/mutation_tests.py has 21 mutations for XXI.1-4 at 5ed4072 (5+5+5+6), 24 at 89ac710..dcdfea6 (XXI.5: +3,
       eleventh checkpoint), 28 from 658b77f (XXI.6: +4).  Our replacement text (R9_REPORT sec. 6 (3)) says "before the review: XXI.1-4 with 21": wrong, it was
       XXI.1-5 with 24.  (Our reviewer took the "before" state from the stale row G27, not from the harness.)
   (2) certificate.txt: RIGHT in substance, their count is loose.  ws_R9/out/certificate.txt prints coordinates of FOUR bridges - those of the Z^4 (profile)
       certificate, with 4, 5, 7, 10 beads [(0,0,1,1;7), (0,0,1,1;8), (0,1,3,3;10), (1,6,10,5;13), recomputed from the coordinates] - of which only the first two
       are among the five of R9.1(e) (4, 5, 9, 9, 11 beads).  The coordinates of all five are in the SCRIPT ws_R9/r9_certificate.py (dict walks), which checks them.
       Our three sentences "Coordinates are in the file" (R9_REPORT l.576), "gives five bridges with coordinates" (R9_ADDENDUM l.193-194), "has five such bridges
       with coordinates" (SCI-REV-0011 sec. 4) are wrong about the output file.  (Their r9/out_their_certificate_check.txt verifies all five from coordinates.)
   (3) inheritance of the ends for clean bridges: RIGHT.  At 24a3c27, Prop 11.69b(a): "The concatenation of Lemma 11.68 of two clean bridges is a clean
       bridge, and its (h,g) is exactly the sum".  Our "(You had half of it ... without the inheritance of the ends)" (SCI-REV-0009 sec. 4, R9_REPORT 4.5) was
       written against 658b77f, where the REPORT had the decomposition only; even there THY-RES-0007 sec. 1.3 already said "and stay clean" as an observation.
       Our R9_ADDENDUM sec. 2 says their proof is right in every step, so no text of ours denies it for the sixteenth checkpoint.
  R9b-T2 (the false parenthesis) applied with our example (lines 5975-5981).
- 05:33:25  ITEM 3, harness RE-RUN (their code from the export, unchanged; r13_10_harness_rerun.sh; out/harness_rerun.log ends with R13_10_DONE; full mode,
  seed 20261124; harness sha256 66cc05bb...; it writes no file): XI.21, XVIII.8, XXV.1, XXV.2, XXV.3 all "survived", exit 0, 0.5-4 s each.
  The five info strings are IDENTICAL to their stored docs/falsification_output.txt at 63e36f7:
   XI.21: instances=200, state=146, const=138, state_not_const=9, minimiser=148, gap=2, domains=100, nonproduct=97, complete_fails=11, sound_domain=55
   XVIII.8: bridges=1312, pairs=1750, nonzero_error=521, with_B=72, two_bonds_differ=8, clean_pairs=1042, cleaned=1508, head1_fails=24, closest_108=0.142
   XXV.1: chains=20, U=80, U_needs_slack=78, Lp=30, Lp_needs_reduction=28, A=20, worst=8.9e-16
   XXV.2: F_cases=100, F_smallest=1.063, F_needs_slack=1, thr=6, block_bound=0.03276, reversal=0.9308
   XXV.3: chains=15, random_f=200, closest=1, expansion in [0.9971, 0.9995]
  FINDING (minor, numbers): the REPORT (Prop 11.18b "How much is gained", lines 2396-2399; Prop 11.18c(a), line 2440-2441) and THY-RES-0011 sec. 2 quote
  for XI.21 "they exist in 153, constant shares ... in 135 of those, the reference minimises the model in 154 - one integrality gap" and "the criterion held
  without shares in 8 of 100".  The harness at the same commit prints 146 / 138 / 148 / two gaps, and 10 of 100 random domains (complete_fails=11 includes
  the explicit two-site example, added after the loop).  The quoted numbers are not those of the stored output; no claim depends on them.
  (XXV.2: 0.9308 and 0.0328 match; XXV.3: [0.997, 0.9995] matches; XVIII.8: 1 312 bridges matches.)
- 05:33:25  ITEM 2, Theorem 11.110(f) (one reading; READ + re-derivation of the sharper end): <EXP> THEORY_REPORT.md 9544-9595, BoxBennett.lean (35 lines, in full),
  SCI-MSG-0023 in full.  ln Z <= ln Z0 - mu + W(mu - lo) = ln Z0 - lo + [W(b) - b], b = mu - lo >= rbar - eta - lo, W(b) - b nonincreasing
  => ln Z <= ln Z0 - rbar + eta + W(rbar - eta - lo): correct, and exactly our deterministic_bracket_sharp (hypothesis lo < rbar - eta stated).
  The gain in [0, 2 eta]; "70 % at 8 k_BT" attributed to us; three redundant hypotheses listed; "at lo = rbar + eta read W(0, v) as 0" not carried (harmless).
  bennett_bracket (BoxBennett.lean) = our bennett_bracket_weights applied; statement = first display of (f) (floor on the support only; no v >= 0).
  Their BennettTwoPoint.lean differs from ours (sha 3688efb6...) in exactly two hunks: the provenance paragraph and the removed #print axioms block.
  Nit: the bracket label of Theorem 11.110 still reads "[(a), (f) K; ...] (BoxClass.lean)" while the text of (f) and THY-RES-0011 say machine-checked.
- 05:40:34  OWN ERROR (resources): the scan "u = 0.5, n = 4000..5050, every n" was launched with an estimate of 9 minutes; at 1.5-1.8 s per size (machine load 4)
  it would have run about 26 minutes, over the 20-minute limit.  Stopped by me after 8 minutes (kill of my own process); its partial log is kept as
  out/sep_scan_u0.5_INCOMPLETE_stopped_not_cited.log and is NOT cited.  Replaced by a window scan (4500..4600, every n) and a coarse scan.
- 05:40:34  ITEM 2, remark (1a): scans with r13_09_separation_scan.py (RE-RUN of our R6 code for C_max from byte-identical copies in ws_R13/r6_copy/ - sha256
  everyn.py 142dd61a..., r6lib.py 9cd6fdb7... - because ws_R6/separation.py appends to ws_R6/data/, outside my write area; OWN LINES for the non-adaptive
  lower bound from the statement of Thm 11.45(b), which agree with R6's column to 1e-6 at every size).  phi = 0.5 (n_o = floor(n/2)), design K64.
  u = 1, every n in 1000..2100 (out/sep_scan_u1.log, complete): first n with C_max < LB: 1370; failures after it at 1371-1376, 1378-1383, 1390, 1397;
        holds at every n from 1398 to 2100.   => "1370" and "1398" CONFIRMED.
  u = 2, every n in 300..760 (out/sep_scan_u2.log, complete): first 518; failures after it at 520-523, 528-531, 537; holds from 538 to 760.
        => "518" and "538" CONFIRMED.
  Table of remark (1a): (1, 1000) 126.26 / 110.90; (1, 1350) 150.76 / 149.02; (1, 1400) 153.96 / 155.02 reproduced (first test run of the driver).
- 05:40:34  LEAN (item 1 (v)): lean/RateCore.lean (Mathlib only; 262 lines) compiles with `lake env lean`: exit 0, no warning, axioms
  [propext, Classical.choice, Quot.sound] for epoch_gain, closed_form, rate_of_epochs.  Two failed first attempts (field_simp did not clear a denominator).
  lean/RateFull.lean = the core (verbatim, generated) + lemma1_top, lemma1, lemma2, epoch_of_stepLE, rate_top, importing proofs.Frontiers.HintRecursion
  (identical in our tree and at 63e36f7): compiles, exit 0, no warning, same three axioms.  rate_top is STATEMENT (a) OF THE RATE for every HintPair with
  h < a and every sequence of levels with the stated hypotheses: T n x <= h + c1/(n + c2) for all n >= 1, x > 0.  One failed attempt (an algebra step).
- 05:40:44  OWN ERROR (rule): in the command that stopped the long scan I wrote `sleep 1` and `sleep 2` in the foreground (3 seconds in all), which the brief
  forbids.  Not repeated.  The replacement scans were started with `&` from that same call (one process: the window 4500..4600, then the coarse scan).
- 05:45:11  LEAN, continued: statement (b) and the cube.  lean/RateFull.lean (740 lines; sha256 90b7a4ff...) now contains, besides the core and rate_top:
  rate_top0 (levels numbered from zero, as exactRec), rate_all0 (statement (b) with the constant L of hint_lower as a hypothesis),
  cube_exactRec_rate_top and cube_exactRec_rate_all (the exact recursion of the cube, nothing assumed; L = 1 from cubeHint_add_mono + cubeHint_zero;
  h < a from cubeHint_lt_cubeNa at 0).  It imports proofs.Frontiers.BoundedAccuracy (-> CubeHintPair -> HintRecursion), all three identical in our tree
  and at 63e36f7.  `lake env lean`: exit 0, 46 s, no error, no warning, no sorry/admit/native_decide/axiom; #print axioms: [propext, Classical.choice,
  Quot.sound] for all eleven theorems; the four final statements printed by #check (out/lean_RateFull.log).  This part compiled at the first attempt.
  (Correction of the previous entry: RateCore.lean has 303 lines, sha256 1c7a0d36...; out/lean_RateCore.log.)
  NOT formalised: the limsup statement; the identification of sup T_k with the tau_k of sec. 11.19; anything about algorithms.
  Caveat: compiled against the .olean files of our tree's existing build (sources identical; the build itself was not re-made - no lake build).
- 05:45:21  Remark (1a), u = 1/2: window scan every n in 4500..4600 (out/sep_scan_u0.5_window.log, complete): NO for 4500-4523, first yes at 4524; failures after
  it at 4525-4528, 4530-4533, 4536-4538, 4541, 4544, 4546, 4549, 4554, 4560, 4565; yes from 4566 to 4600.  Coarse scan every 50 from 4000 to 5050
  (out/sep_scan_u0.5_coarse.log, complete): NO at 4000..4500, yes at 4550..5050.  => "4524" and "4566" CONFIRMED on the window (not every n of 4000..5050
  was scanned by me: 4000-4499 and 4601-5050 only every 50).  All six numbers of remark (1a) reproduced.
- 05:56:11  LEAN, third part: rate_zero (Proposition R13.1 of my report: the same rate for a sequence tau_k obeying the one-level bound at accuracy zero - the
  hypothesis hstep0 of their levels_reach_hint_at_zero - with tau_0 <= a), plus slope_of_stepLE and le_of_forall_lt_frac.  Compiled at the first attempt.
  Final lean/RateFull.lean: 941 lines; `lake env lean`: exit 0, no error, no warning; 13 theorems printed, all [propext, Classical.choice, Quot.sound];
  out/lean_RateFull.log (final).  The part files lean/*_part.lean.txt are the pieces from which RateFull.lean is assembled (core verbatim from RateCore.lean).
- 05:56:11  Report written: docs/science/workstreams/R13_REPORT.md (sections 0-8).  Numbers quoted in it re-read against the logs; spot checks: E_F(0.7, 1) = 0.05404;
  A(eps*/2) = 1.0430 at u = 1 (A/eta = 940 at eta = 0.01 a); Var(sum s)/n = 1.792 at n = 4, p = 0.3; times of r13_04 (8 s), r13_06 (24 s) measured.
  Summary rows of their report (lines 100, 1516) read for the small-slope law and the reversal: both state the limit / "u >= 3" without the qualifications.
- 05:58:43  Report revised after a full re-read (wording of M1, m5, m7, m8; R13.1 now [V]; my B_k also bounds the tau_k of sec. 11.19, so the cube runs test
  rate_zero as well).  Check that nothing was written outside the allowed area: the export has no file newer than my brief; the .lake build files of
  our tree keep their timestamps of Nov 25; `git status --short` (read-only) shows, besides ws_R13/ and R13_REPORT.md, only files of the coordinator
  and of other running workstreams (ws_P7, ws_P8, pi_inference, collaboration files) that I did not touch.
  No tool declined an action during the whole run.

## Index of files (experiments/science/ws_R13/)

  r13_01_cube_recursion.py     own one-sided level recursion of the cube (item 1 (iii))          -> out/cube_u*_k60_r*.{log,json}
  r13_02_run_cube.sh           the six production runs
  r13_03_closed_form.py        constants (mpmath); closed form vs epoch recursion (exact, float)  -> out/closed_form.log
  r13_04_tau2.py               exact tau_2                                                        -> out/tau2.log
  r13_05_blocks_recursion.py   Markov recursion with blocks of 1, 2, 3 sites (item 2, sec. 11.32)  -> out/blocks_recursion.log
  r13_06_small_slope_asym.py   counter-example to Prop 11.117(b) without "symmetric"              -> out/small_slope_asym.log
  r13_07_shares_bruteforce.py  integrality gap, Lean witness, 11.18c(a) example, random test      -> out/shares_bruteforce.log
  r13_08_r9_arith.py           determinants, norms, the four bridges of certificate.txt           -> out/r9_arith.log
  r13_09_separation_scan.py    remark (1a): C_max (R6 code, copies in r6_copy/) vs own LB          -> out/sep_scan_u1.log, _u2.log, _u0.5_window.log, _u0.5_coarse.log
  r13_10_harness_rerun.sh      harness XI.21, XVIII.8, XXV.1-3 from the export                    -> out/harness_rerun.log
  lean/RateCore.lean           Mathlib-only core: epoch_gain, closed_form, rate_of_epochs          -> out/lean_RateCore.log
  lean/RateFull.lean           + lemma1, lemma2, epoch, rate_top, rate_top0, rate_all0, cube_exactRec_rate_top/_all, rate_zero -> out/lean_RateFull.log
  lean/*_part.lean.txt         the pieces RateFull.lean is assembled from
  lean/SoftMinLowerBound_copy.lean  their file + 5 lines                                          -> out/lean_SoftMinLowerBound_copy.log
  thy_copy_nested_R6/          byte-identical copy of their t4_rate.py and its output             (RE-RUN)
  r6_copy/                     byte-identical copies of our ws_R6/everyn.py, r6lib.py              (RE-RUN)
  NOT TO BE CITED: out/sep_scan_u0.5_INCOMPLETE_stopped_not_cited.log, out/test_*.json

- 05:59:35  Final message written (at most 400 words) and handed back to the coordinator.  End of the workstream.
