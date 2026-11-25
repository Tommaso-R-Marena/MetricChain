# R6 working notes (independent review of theory report §§11.18–11.19)

Reviewer: independent referee, workstream R6, science division.
Repository: /home/user/MetricChain at branch research/scientific-translation (theory files at 5ed4072).
Rules: write only here and in docs/science/workstreams/R6_REPORT.md; no state-changing git; no lake build.

## Log

### Step 0 (start)
- Read COMMON.md and R6_brief.md in full.
- Created this directory. Machine: 4 cores, 15 GB, Python 3.13.18.
- Plan: (1) read §11.18–11.19 for the *specification* only (algorithm + statements), not the cost proof;
  (2) write my own accounting; (3) implement myself; (4) then read their proof, H/K reports, referees,
  D45, ENG-RES-0008 and compare.

### Step 1 (reading for the specification only)
Read in THEORY_REPORT.md: lines 3015-3203 (§11.16: Lemma 11.43, Thm 11.44, 11.45, Prop 11.46), 2283-2372 (Thm 11.25),
3528-3653 (§11.18 up to and including the algorithm text of Thm 11.52; NOT the proof at 3654-3724 yet),
3725-3905 (Thm 11.53, 11.54 with proof of 11.54, remarks), 3905-4003 (§11.19 up to statement of Thm 11.56),
4024-4196 (Prop 11.57, Thm 11.58, remarks). NOT yet read: proof of 11.52 (3654-3724), proof of 11.56 (4004-4023),
K_REPORT, H_REPORT, R7, R8, D45, ENG-RES-0008, any implementation.

### Step 2 (my own accounting for Algorithm 2L, written BEFORE reading the proof at 3654-3724)
Setting: Q_n = Q_o x Q_i, m := n_o = floor(phi n), n_i = n - n_o, W(a) fibre average, p(s) = P(W > s),
levels s_j = s_0 e^j, tolerance b = x_last, G = g n, K, J as in the text.

Deterministic facts (hold in EVERY run, no probability):
 (D1) M <= max(K, 2 M_j^neg) at level j [M is doubled only when M < M_j^neg; ell is constant while a level is unpopulated].
 (D2) a level left as populated has s_{i+1} q_i <= 4 e^{b+1} ell (ell after the update); a level left as negligible has
      s_{i+1} q_i <= e^b ell / J.
 (D3) "closing radius": let r* := largest r <= m-1 with Gamma~(r') <= e^{G-b}/4 for all r' <= r*  (Gamma~(r)=E_r(m)/|B(m,r-1)|,
      Gamma~(0)=e^u-1), pi* := 2^{-m}|B(m,r*)|.  If a level is left without closure then q > pi* at that moment.
      Proof: populated: ell >= s_i e^{-b} q/4, tail = s_i 2^{-m} E_r <= s_i q Gamma~(r) (r=r(q); |B(r-1)| < 2^m q), no closure
      => Gamma~(r) > e^{G-b}/4 => r > r* => q > pi*.  negligible: q <= 2K/M <= ell e^b/(J e s_i), tail <= s_i q Gamma~(r)
      <= ell e^b Gamma~(r)/(Je), no closure => Gamma~(r) > Je e^{G-b} => r > r*.  (r = n_o case: q > 1-2^{-m} >= pi*.)
 (D4) hence after leaving level i: ell >= s_i e^{-b} pi*/4 (populated) or ell > J e pi* s_i e^{-b} (negligible, from
      M_i^neg <= M < 2K/pi*).  So at level j=i+1: M_j^neg <= 8 e^2 K J/pi*, and M <= Mbar := 16 e^2 K J / pi* at every level
      (level 0: M <= max(K, 4KJe^{1-b}) <= Mbar).
 Width: U/ell <= 1 + (J+1) 4e^{b+1} + e^G  (populated levels dominate) => accuracy G + ln(4eJ+3)-ish provided b <= G.

Good event: (V1) all inner brackets valid (incl. width); (V2) for all j and M in {K 2^t}: M p(s_j) >= 2K => at least M p(s_j)/2
 of a_1..a_M have W > s_j; (V3) for all j, M, x in b+N: #{i<=M: W(a_i) > s_j e^{-x}} <= max(2 M p(s_j e^{-x}), K/2).
 Chernoff: each (V2) event fails w.p. <= e^{-K/4}; each (V3) event w.p. <= e^{-K/12}.
 Validity lower end: high => W >= L > s_j e^{-b}; N >= K & V3(x=b) => N <= 2 M p(s_j e^{-b}) => s_j e^{-b} N/(2M) <= A (Markov).
 Validity upper end: V1 => (W > s_j => high); V2 => q >= p(s_j) at every (j,M); layer cake + tail lemma (r <= m-1).
 Count: for x in b+N, level j, M <= max(K,2M_j^neg): let i be the level with s_i <= s_j e^{-x} < s_{i+1} (i<j).
   p(s_j e^{-x}) <= p(s_i) <= q_i <= 4e^{b+1} ell_j / s_{i+1};   M <= 4KJe s_j/(ell_j e^b)
   => M p(s_j e^{-x}) <= 16 e^2 K J e^{j-i-1} <= 16 e^2 K J e^x.   (if s_j e^{-x} < s_0: M <= 4KJe e^{x-b} directly.)
   => #{i<=M: W(a_i) > s_j e^{-x}} <= 32 e^2 K J e^x.
 A point is refined to rung l at level j only if W in (s_j e^{-x_{l-1}}, s_j e^{x_{l-1}-b}] (V1).
 => calls at rung l <= min(Mbar, (J+1) 32 e^2 K J e^{x_{l-1}+1}).
 COST (my bound): 1 + Mbar + sum_{l>=1} min(Mbar, (J+1) 32 e^3 K J e^{x_{l-1}}) C_l.
 Exponents: Mbar -> phi theta_na((g-beta)/phi) (Stirling for Gamma~), count -> (1-phi) xi_{l-1}, C_l -> (1-phi) T(xi_l). OK = (11.18.2)+eta_0.
 Termination on the good event: at level J, N=0 and M_J^neg >= 2KJ e^{11} 2^{m} so M reaches K 2^{m+2}, 2^m q < 1, tail=0.
 Things to compare against their text: the constant in the count; delta' and the union bound over inner calls
 (needs #calls <= something like 2^{n+5} n^3 / L !); the abort rule (must be checked BEFORE an inner call);
 b <= G only for n >= beta/((1-phi)(g-beta)); r* = -1 when e^{G-b}/4 < e^u - 1 (bound void for small n).

### Step 3 (read the proof of Thm 11.52, lines 3654-3724, and compared with my Step-2 accounting)
Term by term: their M-dagger = 2K/pi* (mine), their "every M <= 8Je^2 M-dagger" = my Mbar = 16e^2KJ/pi* (identical);
their count 2M_j^neg p(s_j e^-x) <= 16KJe^2 e^x = mine; with V3: 32KJe^2 e^x + 4K (mine: 32e^2KJe^x, the +4K covers M=K);
rounding x_{l-1} into b+N costs a factor e (same as mine); their cost sum_j sum_l min(8Je^2 M-dagger, 32KJe^3 e^{x_{l-1}}+4K)(l+1)C_l
is an over-count of mine (they charge (l+1)C_l per point and sum over levels; I charge each rung once per point).  AGREE.
Small things found while comparing (all minor, to be listed in the report):
 m-a: the case s_j e^{-x} < s_0 (no level below) is not treated in the count of 11.52 (it is in K_REPORT Step 7); trivial fix.
 m-b: the abort test "if the number of queries exceeds the bound" must be made before an inner call (R8 m1 says so for 11.56;
      the text of 11.52 was not changed).
 m-c: failure budget only "for n >= n_0(eta_0)" -> the assembly "first d tuples whose accuracy is at most x" must also require
      d >= n_0(tuple), or the tuple's procedure is not a bracket procedure with failure probability delta' at small d.
 m-d: accuracy bound gn + ln(4eJ+3) needs b <= G, true only for n >= beta/((1-phi)(g-beta)).
 m-e: l = 0 term / reference query missing in the displayed cost sum (x_{-1} undefined).

### Step 4 (derived the 2L+ analysis from the statement of Thm 11.56 before reading K_REPORT 2.4; then read K_REPORT 1-4)
Derived on my own from the four changes: width (2p_u)^n + e^b(e^lam(1+eta)/(1-eta) + eta' + theta); closing radius conditions
[N] Gamma~ <= theta(1-eta)nu0 and [P] min(Gamma~/c_eta, Gamma'') <= theta; Mbar = 2(1+eta)e^lam nu0 K/((1-eta)pi-dagger);
count M_j^neg p(s_j e^-x) <= c_eta^-1 e^lam nu e^x.  All four agree with K_REPORT Steps 4-7.
Read K_REPORT lines 1-650 (sections 0-5 start).  Checked line by line: good event and K (V2,V3 Chernoff constants OK;
number of events (J+1)(m_max+1)(L+2) OK; no circularity J->nu0->r-dagger->pi-dagger->m_max->K->nu,Mbar->delta');
Steps 1-9; Lemma K.4 (a)-(d); Prop K0; Cor K1.b; Prop E (a),(b); Thm K2 (accuracy arithmetic 5.25 c0 <= x/2 - eps OK); Thm K3 iteration.
No error found so far.  D45 read (five accountings: single threshold; v1; v2; v4; CLOSE).  H_REPORT read (2.6 = original 2L, 2.8 = the wrong ones).
NEXT: implement from the spec (K_REPORT 2.2 + theory report 3616-3652) BEFORE reading any implementation; then R7/R8, Lean, ENG-RES-0008.

### Step 5 (coordinator note received mid-work; new theory checkpoint 40c5bd7)
The coordinator informed me that the theory division published checkpoint 40c5bd7 while I work at 5ed4072.  Read (read-only):
`git diff 5ed4072 origin/claude/determined-ride-og1u7j -- docs/workstreams/K_REPORT.md` (errata e1-e4 added) and the two new
remarks after Thm 11.56 in the 40c5bd7 theory report (extracted to scratchpad, lines 4117-4160 of that version).
 (1) New remark "sample-size cap": in every run every sample is K or has fewer than 2 max{e^lam M-dagger, M-ddagger} points,
     M-ddagger = K/((1-eta) pi-ddagger), pi-ddagger = 2^-n_o |B(n_o, r-dagger - Delta)|, Delta = ceil(lam/u)
     (M-ddagger := K 2^n_o/(1-eta) if r-dagger < Delta).  [P], unrefereed.
     MY RE-DERIVATION (done on paper now): correct for r-dagger >= Delta.  Steps checked: level 0 is populated at M=K in every run
     (rung-0 bracket has L > s_0 e^-b because psi(a,0) <= psi_0 + u n_o: no inner call involved) ; case "after negligible": OK;
     case "after populated": p_low > c_eta pi-dagger, Harper radius >= kappa(r-dagger+1), E_{r-1} <= e^-u E_r (term by term, OK),
     tail <= s_{j-1} e^{lam - u Delta} 2^-n_o E_{r-dagger}; [P] at r-dagger gives tail <= theta e^b ell in both sub-cases
     (also for r-dagger = 0 with the convention Gamma~(0) = e^u - 1).  OK.
     EDGE (to test numerically): if r-dagger < Delta and M = M-ddagger = K 2^n_o/(1-eta) exactly lies in the doubling sequence
     (eta = 1/2), then q = 2^-n_o, 2^n_o q = 1 is NOT < 1, the tail is s_j 2^-n_o (e^u - 1) and closure is not forced; the sample
     may then be doubled to exactly 2 M-ddagger: "fewer than" could fail by equality in the corner 1 <= r-dagger < Delta (needs lam > u).
     Also re-derived the 2L version: an unpopulated pass with M >= max{M-dagger, M_j^neg/(4Je)} closes; hence M < 2e M-dagger.  OK.
 (2) New remark "radial landscapes are almost the whole class for the outer loop" (Harper: tail functions of all u-Lipschitz outer
     landscapes = those of landscapes whose level sets are initial segments of the simplicial order).  Consequence for my harness:
     with a simulated inner oracle only the LAW of W(a) matters; I represent an outer landscape by classes (value, probability).
 (3) Flat-instance cost numbers are best-case numbers (K_REPORT erratum e1).
All findings in my report will be tagged with the commit they refer to (5ed4072 unless stated; the cap remark is 40c5bd7).

### Step 6 (own implementation; written before reading any implementation)
Files: r6lib.py (tables, Params2LP, Params2L, ClassInstance, SimOracle, Run engine for 2L+ and 2L), checks.py (run-by-run checks of
every claim of K1 and of 11.52; deterministic claims vs claims on the good event), instances.py (radial profiles), campaign.py
(cells, campaigns), smoke.py, smoke2.py, explore_params.py.  Engine: units = (block, class) with exact counts (Python ints,
chunked binomials beyond 2^61); q, p_low and all radii exact (Fractions/integers); levels/ell/tails in mpmath (40 digits);
brackets float64 logs.  The sample law is represented by classes (value, probability): by the remark of 40c5bd7 (ENG-RES-0008 sec. 5)
only the law of W matters for the outer loop with a simulated oracle.
Checker validated by five mutations (data/MUT_*_7.jsonl, 48 runs each):
  neg_tol -> count inequality (v) violated in 24 runs (+ M_j^neg bound);   noharper -> level left with q <= pi-dagger (1 run) and
  the 40c5bd7 cap violated;   maxform -> width violated in 26 runs;   close_at_no -> every run returns L > U (48/48);
  q_no_eta -> certificate p(s_j) <= q false in 21 runs, 1 invalid bracket.
First results (before the big campaigns): A_small seed 1: 64 runs, 0 violations; A_medium seed 2: 44 runs, 175 negligible levels,
0 violations, max M/M-dagger = 1.91.

### Step 7 (read R7, R8, ENG-RES-0008 after my own derivation and implementation)
R7 (theory division's referee of 11.18): same line-by-line content as my Step 2/3; found the r = n_o closure gap, the abort rule (M1),
the induction (M2).  R8 (referee of K): "proved", ten minor points; own 2L+ implementation, 15 000 simulated runs, three nested levels on Q_9, Q_10.
ENG-RES-0008 (engineering): 7 095 840 mean runs (expectation level, bounded regime, one set of design parameters b=0.5, lam=0.2,
eta=eta'=theta=0.05) + 585 000 literal runs (b=0.5, lam=0.5, eta=1/4, eta'=theta=0.1; (u,n_o) in {(1/2,300),(1,120),(2,48)}) + reduced K.
None of the three tested: invalid inner answers ((V1) is true by construction everywhere), the extensive regime / Algorithm 2L with
the constants of 11.52 at sizes with negligible levels (R7 did 2L; ENG: "not started"), the new cap of 40c5bd7 (theory's harness XVI.4 only).
My campaigns cover exactly these (B_invalid, D_2L, D_2L_off, cap check in every run).

### Step 8 (Lean: statements read, compiled, axioms printed)
lean/R6Axioms.lean (imports BoundedAccuracy, QueryRefinements; `lake env lean`, exit 0, 8 s; output lean/R6Axioms.out).
- `admissible`, `Rstep`, `exactRec` are exactly R[T] of (11.18.2) and T_1 = theta_na, T_{k+1} = min(T_k, R[T_k]) (index shifted by one).
- `exactRec_reaches_hint : 0<u -> 0<g -> g<cubeEstar u -> 0<eta -> exists k, exactRec (cubeNa u) k g < cubeHint u g + eta`  = statement (R).
- cubeNa = klBin(cubeRadius, 1/2), cubeRadius = sSup{rho in [p_u,1/2] : KL(rho||p_u) <= x}; `cubeNa_isLeast_allRadii` identifies it with
  min{KL(rho||1/2): KL(rho||p_u) <= x} for x >= 0.  cubeHint u e = klBin((Lambda_1+e)/u, 1/2).  OK = paper.
- `two_rung_bound` = the iteration of Thm 11.58;  `close_points_bound'`, `width_le`, `populated_part_le`, `certified_lower_sum_le_mean`
  = algebra only (no algorithm, no probability).
- `cube_exact_dip_randomized` = (LB): finite mixture of consistent deterministic query algorithms, counts DISTINCT queried points at g = 0.
- all ten depend on [propext, Classical.choice, Quot.sound] only.
NOT machine-checked (confirmed by reading): the algorithm, the good event, Harper/tail lemmas, closing radius, sample sizes, the count as a
statement about the algorithm, termination, cost sum, Lemma K.4, Prop K0, Cor K1.b, Prop E, Thm K2, the assembly.

### Step 9 (every-n computations: everyn.py, separation.py)  [refers to Thm 11.56/K1, Prop 11.57(a)/K0, Thm 11.45(b), Thm 11.25(a) at 5ed4072]
everyn.py computes, from exact binomial tables for the given n (no asymptotics): C_max of K1 with K0 inner brackets, the plain K0 bracket,
the hinted lower bound and the NON-ADAPTIVE lower bound of Thm 11.45(b), all at the certified accuracy x_out and delta = 0.05.
Design "K64" = the design of K_REPORT 6.4 / ENG-RES-0008 (b=0.5, lam=0.2, eta=eta'=theta=0.05, nu1=2e^u n_o/theta, inner rates eps* 0.85^i, i<40).
CROSS-CHECK of my constants against ENG-RES-0008 (their table "cap C_max at that phi", ln/(n a)), all digits agree:
  u=1: n=1000 phi=.55: 1.1720 (ENG 1.172); n=2000 phi=.5: 0.8700 (0.870); n=4000: 0.7228 (0.723); n=16000: 0.5887 (0.589);
       plain 1.9254/1.3493/1.2303/1.1516/1.0689 (ENG 1.925/1.349/1.230/1.152/1.069); hinted LB 0.3324/0.2857/0.2754/0.2707/0.2649 (0.332/0.286/0.275/0.271/0.265).
  u=2: n=1000: 0.8056 (0.806); 2000: 0.6899 (0.690); 4000: 0.6210 (0.621).   u=0.5: n=4000: 1.0482 (1.048); 8000: 0.8142 (0.814).
  => three independent implementations (K, ENG, mine) agree on every constant of Theorem K1 and of Prop K0.
NEW (not in any report I read): comparison with the non-adaptive LOWER bound (not with the plain bracket, which is an upper bound):
  certified finite-n separation  C_max(two levels, every run, every instance) < LB_na (expected, every non-adaptive algorithm):
  u=1:   n=1380: tie (ln ratio 0.0); n=1400: +1.1; 1700: +14.5; 2000: +28.1; 4000: +120.5; 8000: +316.2; 16000: +722.5   (n<=1350: negative)
  u=2:   n=520: -1.0; n=540: +2.5; 700: +23.1; 1000: +63.2; 4000: +492.3
  u=0.5: n=4500: -0.6; n=4700: +1.9; 5600: +13.3; 8000: +43.4; 11000: +81.8
  (best phi on the grid = 0.50 at the crossover in all three cases; LB_na/(n a) is 0.99-1.02 already at n = 250.)
  The lowered cap of 40c5bd7 changes ln C_max by at most 0.6 at the crossover sizes (it matters where the first term 2Mbar dominates: n=1000, phi=.55: 130.0 -> 120.7).
Outputs: logs/separation_u1.log, _u2.log, _u05.log, data/separation_K64_u*.jsonl.

### Step 10 (brute-force checks of the inputs: check_tail_lemmas.py, logs/check_tail_lemmas.log)
Harper in the form used (|S| >= |B(m,k)| => |N(S)| >= |B(m,k+1)|): all nonempty subsets of Q_1..Q_4 (65 808 sets), 60 000 random/structured
subsets of Q_5..Q_7: 0 violations.  Lemma K.1(a),(b) at every threshold of 960 random u-Lipschitz functions on Q_4..Q_10 (34 873 + 35 833
thresholds): 0 violations, equality attained (ratio 1.000000).  Lemma K.4(a),(b) and (3.0) on exact tables, m <= 2000, u in {.5,1,2}, 4 values
of eta: 22 583 cases, 0 violations (largest ratios 0.886, 0.854, 0.264).

### Step 11 (the cap remark of 40c5bd7, edge case analysed on paper)
Degenerate branch r-dagger < Delta: the published sentence covers passes with 2^{n_o} q < 1 only; at M = M-ddagger exactly, 2^{n_o} q = 1,
r = 0, tail = s_j 2^{-n_o} E_0.  I close it: for r-dagger >= 1, E_0 <= E_1/(m+2) <= E_{r-dagger}/3, so with lam <= 1:
tail <= s_{j-1} e^lam 2^{-n_o} E_0 < s_{j-1} 2^{-n_o} E_{r-dagger} <= theta e^b ell by [P] at r-dagger and the bound on ell after a populated
level; for r-dagger in {0, -1}: M-dagger >= M-ddagger and the cap is 2 e^lam M-dagger > 2 M-ddagger >= every sample.  So the remark is true
as stated (given lam <= 1, which is a hypothesis of Thm 11.56); the proof has one uncovered pass, closed here.  MINOR.

### Step 12 (end-to-end replication of published trajectories with my literal engine: flat_exact.py)
Flat instance, design K64, inner behaviour "bottom", K0 costs; my engine unchanged (one class, exact block sizes).
  u=1 n=1000 phi=0.55: ln(cost)/(n a) = 0.9788           (ENG-RES-0008 table "flat instance at that phi": 0.979)
  u=1 n=1000 phi=0.80: 0.7013, ln M/(n_o a) = 0.756, closing radius 255, r-dagger 180, 5003 populated / 223 negligible levels
                       (ENG-RES-0008 mechanism table: 0.701, 0.756, 255 (180, 215), 5003 / 223 -- identical in every number)
  u=1 n=4000 phi=0.50: 0.6872                             (ENG: 0.687)
(I have not read their code; K_REPORT's own table has 0.701 at n=1000 as well.)  Remaining cells stopped to free CPU (machine load 10+).

### Step 13 (campaign results so far; machine heavily loaded by other workstreams, my campaigns use 2 processes)
A_small seed 11: 1600 runs (8 cells, n_o 10..40, theorem constants, 17 profile families x 10 valid inner behaviours): 1600 closed,
  0 deterministic violations, 0 violations on the good event, good event never failed; 327 926 populated and 180 negligible levels;
  closures: 232 at a populated pass, 1368 at an unpopulated one, 343 with empty tail; max M/M-dagger 1.98, max M/cap(40c5bd7) 0.84,
  max count ratio (v) 0.869, max calls/bound 0.125.
A_ties seed 12: 500 runs (dyadic lam, u n/lam integer, flat fibres, grid profiles): 451 closed, 49 discarded (a block would exceed the
  sampler limit 2^83), 0 violations, 1819 negligible levels in 134 runs.

### Step 14 (prior-art searches, 25 Nov 2026, generic queries only)
(1) Harper's theorem, statement: search summary + the abstract-level statements quoted by the search tool from arXiv:1806.11061 (Raty),
    arXiv:1808.02572 (Przykucki-Roberts): "|N(A)| >= |N(B)| for B the initial segment of the simplicial order with |B| = |A|"; closed-neighbourhood
    version as well.  [search snippet]  Harper 1966 itself not retrieved.
(2) Kaas-Buhrman 1980 (Statistica Neerlandica 34(1) 13-18): bibliographic data confirmed [search snippet]; the floor/ceil statement of the
    median is attributed to it by secondary sources only (not confirmed from the paper).
(3) Mathe-Novak, "Simple Monte Carlo and the Metropolis Algorithm", arXiv math/0611285: abstract read through a fetch tool: "adaptive methods are
    much better than nonadaptive ones ... the curse of dimension (for nonadaptive methods) can be broken by adaption" [abstract].
(4) query "adaptive versus non-adaptive query complexity estimating partition function Lipschitz function Hamming cube exponential separation
    isoperimetric layer cake algorithm": nothing on this problem [search snippets only]; "not found", not "new".

### Step 15 (cap remark of 40c5bd7, degenerate branch: capcorner.py, seeds 41-43, 4500 runs; data/capcorner_4*.json)
Small outer cubes n_o in 3..12, lam = 1 > u in {0.15,0.2,0.3,0.45}, eta = 1/2 (M-ddagger = K 2^{n_o+1} is in the doubling sequence),
theta in {0.003..1}, nu1 in {1, 30, 2e^u n_o/theta, 1e4}, K partly reduced, valid and invalid inner behaviours.
 - degenerate branch (r-dagger < Delta) in 4151 of 4500 runs; r-dagger >= 1 in 1801 of them.
 - cap 2 max{e^lam M-dagger, M-ddagger} never reached (largest M/cap = 0.5); no deterministic claim violated.
 - r-dagger >= 1: 193 unpopulated passes with M = M-ddagger exactly; all 193 closed (as proved in my Step 11).
 - r-dagger in {0,-1}: the unpopulated pass at M = M-ddagger did NOT close 1255 times and the sample was then doubled to exactly
   2 M-ddagger in 1133 runs: the sentence of the published proof "at level j the size is doubled only below M-ddagger" is false there
   (2^{n_o} q = 1 is not < 1); the STATEMENT is unaffected because then the cap is 2 e^lam M-dagger >= 2e M-ddagger (observed ratio 1/e).

### Step 16 (off the good event: invalid inner answers; the abort rule exercised for the first time)
B_invalid seed 15 (400 runs; 7 cells incl. n_o = 100, 80, 400; invalid inner behaviours: bracket above W, below W, 2.5x too wide, the trivial
  bracket again, mixtures): 195 closed (159 of them with an invalid final bracket, as allowed off the good event), 21 closed with L > U,
  179 aborted ("unclassified at the last rung"), 5 discarded (sampler limit).  Deterministic claims of K1 -- (iii) closing radius > r-dagger at
  every level left, (iv) M <= max(K, 2M^neg), M^neg <= (1+eta)e^lam nu0 M-dagger, M <= Mbar, the cap of 40c5bd7, the width of every bracket
  returned through the closure test, queries <= C_max -- held in ALL 395 runs.
B_lazy (new behaviour LAZY: returns the rung-0 bracket at every rung but the last, a valid one at the last rung; so every point that needs any
  refinement is driven to the most expensive rung):
  seed 18, rung costs 10^l: 59 runs, none aborted, queries <= 0.021 C_vi  (the bound is dominated by Mbar*C_{L-1}; the abort is not needed).
  seed 19, STEEP rung costs C_l = e^{80 l} (the regime of the theorems: the last rung dominates): 60 runs, 33 ABORTED ON THE QUERY BUDGET
  (sample sizes e^24.5 .. e^28.6 > (J+1) cnt(x_{L-1})), 27 closed; queries <= C_max in all 60 (largest ln q - ln C_max = -0.006);
  0 deterministic violations.  => off the good event the cost WOULD exceed C_max without the abort rule (R7's M1 is not a formality),
  and the rule "test before the call" keeps it below.  Nobody had exercised this branch (R8: "no abort"; ENG: "aborted: 0").

### Step 17 (report drafted while the queue runs; fixes to my own tooling)
- R6_REPORT.md: sections 0, 1, 2.1-2.9, 4-8 written; section 3 (numerics) to be filled when the queue (run_rest2.sh, run_rest3.sh) ends.
  WARNING to myself: the run counts in section 1 of the report were provisional when first written; they must be replaced by the
  final numbers of summarise_all.py before the report is declared finished.
- checks.check_2L originally looped over all x in b + N for every pass (O(J^2) thresholds): replaced by the thresholds the proof uses
  (x = b and x_{l-1} rounded up into b + N); the first D_2L campaign (2 runs in 7 minutes) was discarded and is re-run by run_rest3.sh.
- a patch of mine broke the import lines of everyn.py/adversarial.py/separation.py/flat_exact.py for about one minute (HERE became a tuple);
  repaired and re-tested (everyn.py reproduces 1.6306 at u=1, n=500, phi=.5); no campaign imported these files in that minute.
- partial B_reducedK (118 runs): events of the proof fail in 22/40 runs at K=8, 5/40 at K=20, 0/38 at K=50; no claim violated on runs where they hold.

### Step 18 (independent numerics of the exponents: tau2.py; three levels: three.py)
tau2.py: tau_2/a = 0.5001 (u=1/2, phi=.500), 0.5004 (u=1, phi=.500), 0.5056 (u=2, phi=.494)  [reports: 0.5001, 0.5004-0.5006, 0.5056-0.5057];
  identity theta_na(e + theta_hint(e)) = theta_hint(e): max error 4e-12 on 2001 accuracies; Prop 11.57(c) (no level below h, T = theta_hint):
  min over 999 values of phi of [sup_gamma bracket - h] = +7.6e-6, +2.8e-5, +7.8e-5 > 0.
three.py (three nested levels, real randomness at every level, constants of the theorems, pool of middle runs per fibre): first test,
  2 outer runs, 48 middle runs, 4 073 472 real bottom brackets: all valid, all within certified width, no claim violated.

### Step 19 (reading completed; report generator)
- Read the rest of K_REPORT.md (lines 648-998: section 5 remainder, 6.1-6.8, 7, 8, 9, summary) -- after my own implementation and
  numerics; nothing there changes a verdict.  K's own runs report samples up to 4.5 M-dagger (6.2) and 3.9 M-dagger (6.8).
- Proofread R6_REPORT.md sections 0-2.9; fixed the width sentence in (D2) and the cap sentence in Theorem R6.1.
- make_section3.py computes every run count of section 3 from the data files; fill_report.py writes sections 3.2, 3.4, 3.6-3.8 into
  the report from data/summary_all.json (it asserts the sentences that are claims about the data: every valid run closed, good event
  never failed with theorem constants, no violation).  Preview written to the scratchpad; the report itself is filled when the queue ends.
- D_2L_off finished: 210 runs (2L, reduced K and/or invalid answers).

### Step 20 (cross-check of the lower bounds of the separation table: crosscheck_lb.py)
The hinted and the non-adaptive lower bounds recomputed directly from the definitions of Delta_k and D_R with float64 logarithms
(scipy gammaln / logsumexp), sharing nothing with r6lib.Tables: 184 rows of data/separation_K64_u*.jsonl, k* and R identical in every row,
largest difference of ln(lower bound) 1.2e-11.  (My first version of the cross-check overflowed in expm1 for u(k+1-j) > 709 and reported
false mismatches of k*; fixed with ln(e^y - 1) = y + log1p(-e^-y).)
Crossover cells: u=1 n=1400: R = 381 (R/n = .2721, p_u = .2689), ln LB_na = 155.023; u=2 n=540: R = 67, 176.477; u=1/2 n=4700: R = 1784, 141.539.
