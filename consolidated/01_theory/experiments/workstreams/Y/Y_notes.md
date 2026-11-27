# Workstream Y — notes (appended after every step)

## 0. Start (reading)
- Read brief; theory report §11.26 (Thms 11.95, 11.97-11.99, 11.101; Props 11.100, 11.102, 11.103); W_REPORT §§1-5; wv_lib.py.
- Conventions fixed from §11.26: class C = {psi(x) - psi(y) <= d(x,y)}; A = E_pi e^{-psi}; site function
  F*_j(t) = max_M -t ln sum_a (sum_phi M(phi) pi_phi(a)^t)^(1/t) = (1-t) C_t(vertex channel) = min_Q max_phi (1-t) D_t(pi_phi||Q);
  E = lim F*/t (t->0) = max_M -ln sum_a prod_phi pi_phi(a)^M(phi); a = Shannon capacity of vertex channel;
  R^(e) = max_{0<=t<=1}[F*(t) - t e]; h = R^(0); S(e) = e + R^(e); theta_na = R^ o S^{-1}; theta_na(x) = max_{tau<1}(F*(tau) - tau x)/(1-tau).
- Theorems of 11.26 hold for any alphabets, site laws of full support, envelopes with zero diagonal + triangle inequality
  (not nec. symmetric), several site types.  => block of L sites = super-site with alphabet S^L: allowed.

## 0b. Plan after reading (ideas, NOT yet verified — each to be tested numerically before use)
Notation: binary symmetric chain, spins s=+-1, pi(s) ~ exp(K' sum s_i s_{i+1}), K'=K/2, e^K=(1-p)/p; site-wise label sigma in {+-1}^n:
phi_sigma(s) = -(u/2) sum sigma_i s_i (u-Lipschitz), Gibbs law = Ising chain in field (u/2)sigma_i (RFIM chain), Z(sigma) its partition fn.
(i)  (U): A_pi(psi) = A_rho(psi+g)/A_rho(g), rho = product of free-b.c. block laws, g = cut bonds; psi+g in C_{d+}, d+ = d + K at both ends of each block.
(ii) (L'): with gaps m, psi' in C_{d-} on blocks (d- = d - kappa_m at block ends, kappa_m = ln((1+lam^{m+1})/(1-lam^{m+1})), lam=1-2p)
     embeds EXACTLY: psi = psi' + sum ln rho_m(ends) in C_d(chain), A_pi(psi) = A_{prod of block marginals}(psi').  (L) = accuracy version.
(iii) idea: the lower bound for ALL algorithms needs no product structure: Thm 11.27(b) [V] + proof of Thm 11.99 apply to the WHOLE chain as one
     super-site: cost >= (1-2 delta) exp(-t eps + F*_n(t)), F*_n = (1-t) C_t(vertex channel of n-chain).  Threshold: Thm 11.28 remark (i).
(iv) idea: exact sub/super-additivity.  F+_L(t) := F*[free-b.c. block law; d+]  is SUBadditive in L (monotone in the family + product theorem);
     F-_L(t) := F*[stationary block marginal; d-] is SUPERadditive.  => monotone brackets F-_L/L <= F_inf <= F+_L/L, gap <= t*c/L.
(v)  idea: Lyapunov form.  With M ~ M0(sigma) Z(sigma)^t, M0 symmetric Markov (coupling c):
     G_t(M) = ln E_{beta~p_c}[Xi_{K',h}(beta)^t] - t ln E_{b~p}[Xi_{c,th}(b)^{1/t}] - t ln Z0(K') + ln Z0(c),  h=u/2,
     Xi_{kappa,eta}(b) = partition fn of an Ising chain with bonds kappa*b_i in uniform field eta  (moment Lyapunov exponents of 2x2 products).
     c=0:  G/n -> Lambda(t) - t ln 2cosh K' - ln cosh(t u/2) <= cube value (Jensen), hardest instance = zero residual.
(vi) idea: threshold.  E_n >= ln Z_n(h)/Z_n(0) (two labels sigma = +-1 uniform; Q=pi optimal by symmetry+convexity) -> per site
     E_F = ln[lambda_max(K',h)/(2cosh K')] > ln cosh(u/2) for K != 0.   p=0.3,u=1: 0.2324 vs 0.1201.  Conjecture E_inf = E_F (test n<=5).
(vii) small-u heuristic: F_inf(t) ~ t(1-t)(u^2/8)*chi, chi = e^{|K|} (labels constant on long blocks) => at SMALL slopes the interaction INCREASES all exponents;
     K -> infinity at fixed u: cost exponents -> 0.  So the direction at u=1 must be computed.
(viii) idea: Markov DP ("one-sided slack"): F*_n(t) <= (n/L) F*[block law pi(.|prev letter); slopes (u,..,u,u*)], u* = u + g(u*),
     g(x) = ln[((1-p)e^x+p)/(p e^x+1-p)] < K.  p=0.3: u*=1.526.
Order of work: Step 0 controls -> Step 1 brute force of (U),(L),(L') -> block vertices L<=4 -> tables -> Lyapunov bounds.

## Step 0 — controls (DONE; code/y00_controls.py, out/y00_controls.txt, 108 s)
- Own library code/ylib.py: Arimoto iteration for the Renyi form with a duality bracket [lower(M), upper(Q_M)], exponentiated gradient
  for E, Blahut-Arimoto for a; independent inner solvers: SLSQP primal, and the game LP at the Renyi centre.
- Cube u=1 from the site function: h = 0.0291391 (t* = 0.4900), a = 0.1109441, E = 0.1201145  == controls 0.029139 / 0.110944 / 0.120115.
- Block of L=2 independent uniform sites as ONE super-site (4 letters, Hamming envelope): 6 vertices (4 additive + 2 non-additive
  = +-u*1[x1 != x2], i.e. a PAIR term); per-site h, a, E identical to the cube to 1e-7.  L=3: 38 vertices (8 additive), same values.
  Non-additive vertices get weight ~1e-11 in the optimal M and the additive ones alone give the same value: for a PRODUCT law they
  carry no weight (consistent with the product theorem; the non-additive ones alone give 1/2 resp. 2/3 of the values).
- Vertex enumeration: (i) spanning trees of tight edges with signs (complete, L<=3, any weights), (ii) integer height functions
  (uniform slope; counts 2, 6, 38, 990 for L=1..4), (iii) wv_lib.vertices (reference file, reused only here as a check, q=4): agree.
  With unequal weights more vertices: (1.847,1,1.847): 120; (0.677,1,0.677): 96; (1,1,1.526): 96.
- Field control 'bin' (0.7,0.3): h=0.0250335, a=0.0953005, E=0.1031310 == theory report table.

## Step 1 — the two reductions (statements + brute force DONE; code/y01_reductions.py, out/y01_reductions.txt, 6.5 s)
Setting: pi(x) ~ exp(-sum f_i(x_i) - sum J_i(x_i,x_{i+1})), inhomogeneous allowed; site envelopes d_i (quasi-metrics).
(U) cuts c in K; any gauge J_c = r_c(a)+s_c(b)+J0_c(a,b); rho = prod over blocks of [block Gibbs law with r_c, s_c as end fields];
    g = sum_c J0_c(x_c,x_{c+1}).  Then pi = rho e^{-g}/E_rho e^{-g},  A_pi(psi) = A_rho(psi+g)/A_rho(g)  (known denominator),
    psi in C_d => psi+g in C_{d+},  d+_c = d_c + delta^-_c,  d+_{c+1} = d_{c+1} + delta^+_c,
    delta^-_c(a,a') = max_b[J0(a,b)-J0(a',b)],  delta^+_c(b,b') = max_a[J0(a,b)-J0(a,b')]  (zero diagonal, triangle ineq., may be negative;
    symmetric version max|.| is a pseudo-metric).  Brute force: 432 residuals/36 chains (n=8,9,10 binary; n=6 ternary; random gauge):
    identity 1.3e-15, admissibility violation 7e-15 (=0), d+ is ATTAINED by cones (slack left -4e-15); control: without slack 432/432 violate d.
    Kind preserved: same query points => non-adaptive stays non-adaptive; hint psi <-> psi+g; output shifted by the known ln A_rho(g).
(L) blocks B_1..B_k with gaps; marginal of pi on blocks = prod pi_{B_j} * prod_j rho_j(x_{end j}, x_{start j+1}),
    rho_j(a,b) = P(a,b)/(P(a)P(b)) [two-site marginal over product of one-site marginals].
    For psi' in C_{d_B}: sum min ln rho_j <= ln A_pi(psi' o proj) - ln A_prod(psi') <= sum max ln rho_j.  Brute force: identity 6e-16,
    bound never violated (432 residuals).  => a (eps/2,delta)-correct chain algorithm is ((eps + sum_j osc ln rho_j)/2, delta)-correct
    for the block product (centre the output).  Kind preserved.
(L') [new variant, exact, no loss of accuracy]: psi' in C_{d-} (d- = d_B minus eps^-_j at block ends / eps^+_j at block starts,
    eps^-_j(a,a') = max_b[ln rho_j(a,b) - ln rho_j(a',b)], eps^+ similarly) => psi = psi' + sum_j ln rho_j in C_d(chain) and
    A_pi(psi) = A_prod(psi') EXACTLY.  Brute force: 252 residuals, violation 2e-15, identity 3e-15; control: psi' in C_d fails 225/252.
Binary symmetric chain: delta^+- = K*1[a!=a'] (K = ln((1-p)/p)); rho_m(a,b) = 1 +- lam^(m+1), lam = 1-2p;
    eps^+- = kappa_m*1[a!=a'], kappa_m = ln((1+lam^(m+1))/(1-lam^(m+1))) (kappa_0 = K).
    p=0.3: kappa = 0.847 0.323 0.128 0.051 0.021 0.008;  p=0.2: 1.386 0.754 0.439 0.261 0.156 0.093;  p=0.1: 2.197 1.516 1.131 0.870 0.681 0.537.
    When osc J > site envelope: (U) is unaffected (d+ is still an envelope; the bound is just weak); (L') needs u > kappa_m at block ends
    (u > 2 kappa_m for L=1), i.e. gaps m>=1 for p=0.2 and m>=3 for p=0.1 at u=1; (L) (accuracy version) always works.

## Step 3 (first pass, p=0.4 only; code/y02_blocks.py — too slow in its first two versions, see below)
- (U)  L=1,2,3: h <= 0.0830, 0.0580, 0.0495;  a <= 0.2872, 0.1979, 0.1718;  E <= 0.3638, 0.2644, 0.2324   (cube: 0.02914, 0.11094, 0.12011)
- (DP) L=1,2,3: h <= 0.04053, 0.03889, 0.03736; a <= 0.1509, 0.1351, 0.1297; E <= 0.16935, 0.16921, 0.16917  [DP = idea (viii), proof to be written, test pending]
- plain blocks (stationary law, slopes u; not a bound) L=1,2,3: h = 0.029139, 0.032875, 0.033599; a = 0.110944, 0.115521, 0.116473; E = 0.120115, 0.141026, 0.150050
- (L') best over m: L=1: h>=0.0105 (m=1); L=2: 0.0189 (m=1); L=3: 0.0231 (m=1); a>=0.0799, E>=0.1020 (L=3,m=1).  (L) (accuracy version) is weaker for small m, equal for large m.
- FIRST SIGNS: plain block values INCREASE with L above the cube; E_F(p=0.4) = 0.169127 (closed form) vs DP upper 0.16917 at L=3
  => E is pinned to 4 digits: E(p=0.4) = 0.1691 > 0.1201.  The interaction RAISES the threshold.  h, a: block brackets [0.0231, 0.0374] straddle the cube.
- Own errors: (1) y02 v1: h certified by a grid bound with coarse intervals next to the fine window -> upper 3% too large (0.030108 for the cube);
  replaced by the bracket at t* (not a certificate over all t; coarse scan checks for several local maxima).  (2) tolerances 1e-12 with
  4e5 iterations in E/capacity made the script exceed 10 min twice; (3) an SLSQP active-set solver was slower (37 s on one case) than
  the multiplicative solvers; kept only as an independent check (agreement 1e-9 on 10 cases).
- NB: git status shows docs/THEORY_REPORT.md etc. modified at 19:21 by someone else (coordinator) while my script ran; I did not touch the repository.

## Step 3b/4 — Lyapunov lower bounds (code/ylyap.py, code/y03_lyapunov.py, out/y03_lyapunov.txt, 26 s)
- Transfer-operator moment Lyapunov exponents: N=32,48,64 agree to 1e-12; exact increments ln E_n - ln E_{n-1} (n=13,15) approach them
  (slowly for large order r; to be double-checked with the second eigenvalue).  Formula (v) for G_t(M_c) against the brute-force Renyi form on
  n=8 (256 labels x 256 configurations), 27 cases: 1.9e-15.
- n -> infinity, u=1, labels site-wise, label law = Z^t-tilted symmetric Markov (coupling c), maximised over (t,c):
    p=0.4: h >= 0.033503 (t*=0.458,c*=0.774)  a >= 0.116817  E >= E_F = 0.169127     (cube 0.029139 / 0.110944 / 0.120115)
    p=0.3: h >= 0.038695 (t*=0.431,c*=0.859)  a >= 0.123875  E >= 0.232400
    p=0.2: h >= 0.041770 (t*=0.402,c*=0.861)  a >= 0.122445  E >= 0.310766
    p=0.1: h >= 0.039608 (t*=0.364,c*=0.833)  a >= 0.101876  E >= 0.401719
  With c=0 (i.i.d. labels; hardest instance = zero residual) the value is BELOW the cube (0.028907, 0.028151, 0.026626, 0.023418): Jensen.
  => ANSWER (lower-bound side, depends only on Thm 11.27(b) [V] + algebra + numerics): a nearest-neighbour interaction without a field
     RAISES h (>= +33% at p=0.3) and E (x1.93 at p=0.3); the hardest instance is NOT the zero residual (correlated labels c*~0.8).
- n=8, all 256 site-wise labels, optimal law (Arimoto): p=0.3,t=0.45: F = 0.32113 (0.04014/site) vs best tilted Markov 0.30867 vs c=0 0.22484 vs cube 0.23160.

## Steps 2/4 — exact short chains as one super-site (code/y04_exact_small_n.py 4, out/y04_exact_n4.txt, 339 s)
- n<=4 (990 vertices at n=4), p=0.4,0.3,0.1, t=0.25,0.45,0.65: F*_n(all vertices) = F*_n(site-wise labels only) to 1e-7; non-additive weight <1e-8.
  E_n likewise, and E_n = ln Z_n(h)/Z_n(0) to 1e-11 in all 12 cases  => conjecture E_n = ln Z_n(u/2)/Z_n(0) for every n (so E_inf = E_F).
- EXCEPTION: a_4 at p=0.1: 0.5726559 (all vertices) > 0.5626014 (site-wise only), non-additive weight 0.092.  So non-additive vertices DO carry
  weight for a chain (strong coupling, t -> 1).  Not at p=0.4, 0.3 for n<=4.
- DP bound (idea viii, finite-n form with d*_n=u, d*_i=u+g(d*_{i+1})) holds in all 36+24 cases; E: DP is within 1e-4..2e-2 of E_n.
- almost-additivity: max|F*_{n1+n2}-F*_{n1}-F*_{n2}|/(tK) = 0.07, 0.09, 0.08 (<= 1 required).
- per-site F*_n(0.45)/n: p=0.4: .02895 .03280 .03359 .03354; p=0.3: .02895 .03711 .03984 .04017; p=0.1: .02895 .04498 .05193 .05334 (n=1..4)
  (not monotone in n at p=0.4).

## Step 3 — block bounds L<=3, all p (code/y02_blocks.py; out/y02_blocks_a.txt [p=.5,.4,.3; 353 s], out/y02_blocks_b.txt [p=.2,.1; 209 s])
Per site, u=1.  U = algorithmic upper reduction (slack K at both block ends); DP = Markov-recursion upper bound on the game function
(one-sided slack g(u*)); L' = lower reduction with gaps (best over m<=5); Lyap = Lyapunov lower bound (y03).
 p   | h: L'(L=3)  Lyap     DP(L=1,2,3)                 U(L=1,2,3)              | a: L'     Lyap     DP(L=3)  U(L=3)  | E: L'     E_F      DP(L=3)   U(L=3)
 0.5 | all = cube: 0.029139 / 0.110944 / 0.120115
 0.4 | 0.02307   0.03350  0.04053 0.03889 0.03736     0.08302 0.05804 0.04948 | 0.07987 0.11682 0.12970 0.17181 | 0.10199 0.16913 0.16917 0.23243
 0.3 | 0.02088   0.03870  0.05484 0.05180 0.04902     0.15031 0.09387 0.07428 | 0.06978 0.12388 0.15401 0.23680 | 0.09375 0.23240 0.23285 0.39226
 0.2 | 0.01742   0.04177  0.07202 0.06672 0.06197     0.22525 0.13205 0.10025 | 0.05681 0.12245 0.17747 0.29177 | 0.07830 0.31077 0.31376 0.61087
 0.1 | 0.01020   0.03961  0.09157 0.08299 0.07542     0.31125 0.17250 0.12692 | 0.03518 0.10188 0.19678 0.32951 | 0.04459 0.40172 0.41799 0.93694
Brackets [best lower, best upper]:  p=0.4: h [0.0335,0.0374] a [0.1168,0.1297] E [0.16913,0.16917];  p=0.3: h [0.0387,0.0490] a [0.1239,0.1540] E [0.23240,0.23285];
  p=0.2: h [0.0418,0.0620] a [0.1224,0.1775] E [0.3108,0.3138];  p=0.1: h [0.0396,0.0754] a [0.1019,0.1968] E [0.4017,0.4180].
Reading: the block reductions (U),(L') with L<=3 alone give brackets that contain the cube value (factor 2-10 wide): they do NOT decide the question;
 the decision comes from the Lyapunov lower bound (h, a, E above the cube; a at p=0.1 undecided) and the DP upper bound (E pinned to 2e-4..4e-2 relative).
(L) (accuracy version) is weaker than (L') at small m and coincides with it at large m (numbers in the out files).
Plain blocks (stationary law, slopes u; not bounds) L=1,2,3: p=0.2: h .02914 .04122 .04601; p=0.1: .02914 .04504 .05197.

## Step 4 — structure (code/y05_structure.py, out/y05_structure_n4.txt, 43 s; code/y06_sitewise_long.py 0.3 0.431, out/y06_sitewise_p0.3.txt, 404 s)
- n=4 (all 990 vertices): at t=0.45 the optimal M sits on the TWO uniform-field labels (p=0.3, 0.1) resp. 4 labels (p=0.4);
  the Renyi centre is then pi*cosh(t h m)^(1/t) (m = magnetisation): the hardest instance gamma* = -(1/t) ln cosh(t h m) is a FUNCTION OF THE TYPE
  (no site terms; pair terms: Walsh norm 0.245 at order 2, 0.009 at order 4; nn pair coefficient -0.100), and Q* is NOT Markov:
  I(x1;x3|x2) = 2.9e-3 (p=0.4), 5.7e-3 (p=0.3), 1.2e-3 (p=0.1); pi: 0.
- capacity, n=4: p=0.4/0.3: 8-10 additive labels (uniform fields heaviest: 0.21 / 0.29 each).  p=0.1: support = {up, down} (0.454 each) +
  ONE NON-ADDITIVE vertex (0.092): f(x) = -min(|x|, 4-|x|) = -(distance to the two ground states): a third "paramagnetic" label.
- site-wise labels on whole chains, optimal law (exact within the family), p=0.3, t=0.431:
    n=6: 0.039856/site; n=8: 0.040183; n=10: 0.040243; n=12: 0.040328 [bracket 3e-5];  increments (F_n-F_{n-2})/2: 0.04117, 0.04048, 0.04075
    best tilted Markov at the same n: 0.03906, 0.03866, 0.03855, 0.03852 -> limit 0.038693 (Lyapunov).
  => the first-order Markov label family loses about 5%: the optimal law is SPARSE (8, 12, 18, 40 labels of 64..4096), flips rarely
  (P(flip at the middle bond) = 0.085 at n=12, Markov optimum c*=0.86 has 0.152).  Best ESTIMATE [numerical, not a bound] of F_inf(0.431) at p=0.3: 0.0405-0.041.
  The centre stays non-Markov (I = 2e-3 at n=12).
- Own slip: started the n=5 run with ulimit -v 6000000 instead of the prescribed 4000000; killed after seconds and restarted with 4000000.

## Step 4 cont. — n=5 with all 395094 vertices (code/y05_structure.py 5, out/y05_structure_n5.txt, 88 s)
- p=0.3: F*_5(0.45) = 0.1984112 with all vertices = site-wise only; the site-wise centre is a dual certificate over ALL vertices (max (1-t)D_t = 0.1984112).
  E_5 = 1.0091780 = ln Z_5(h)/Z_5(0) (certificate over all vertices).  a_5 = 0.6397285, site-wise labels suffice.
- p=0.1: t=0.45 site-wise suffice (0.2592261); t=0.65: site-wise optimum 0.1939640 but max over all vertices of the dual value at the site-wise
  centre is 0.2500923; t=0.85: 0.0928291 vs 0.1066245 => KKT violated: NON-ADDITIVE VERTICES CARRY WEIGHT at p=0.1 for t>=0.65 (n=5) and for a (n=4).
  => "site-wise labels are optimal" is FALSE in general for chains [numerical, exact enumeration]; true in every case computed for p >= 0.3, n <= 5.

## Step 3b cont. — label laws i.i.d. over blocks with the exact boundary correction (code/y07_block_labels.py, out/y07_block_labels_p0.3.txt, 134 s)
- Formula: F_inf(t) >= [G_L(M_L) + Lam_blk(t) - t ln lam_max(B_Q rho0)]/L (M = prod M_L tilted by c_phi^t; c_phi = product of 2x2 matrices B_phi rho0).
  Validation: brute-force Renyi form on n=6 (64 labels) and n=9 (512 labels): agreement 1e-12; operator vs exact increment 1e-10.
- p=0.3, t=0.431: two labels per block (domains of fixed length L): best L=4: 0.039419; <=1 wall per block: L=10: 0.039786;
  <=2 walls: L=6..14: 0.039319 0.039776 0.039919 0.040051 0.040114 (still rising).  After refining t: h >= 0.040115 (t=0.434) = x1.377 of the cube.
  a >= 0.126444 (t=0.99; <=2 walls, L=8) = x1.140.
  (tilted Markov: 0.038693; exact site-wise optimum on n=12: 0.040328/site; increments 0.0405-0.0408.)

## Step 3b cont. — block-label lower bounds, all p (out/y07_block_labels_p0.4_0.2_0.1.txt, 359 s)
 p=0.4: h >= 0.034026 (<=2 walls, L=12; t=0.459) x1.168;  a >= 0.116547 (tilted Markov gives 0.116817)
 p=0.3: h >= 0.040115 (L=14; t=0.434) x1.377;             a >= 0.126444
 p=0.2: h >= 0.044599 (L=14; t=0.409) x1.531;             a >= 0.129797
 p=0.1: h >= 0.044378 (L=14; t=0.380) x1.523;             a >= 0.116632  (now ABOVE the cube 0.110944: a is decided at p=0.1 too)
 best fixed domain length (2 labels per block): L=3 (p=0.4), 4 (0.3), 5 (0.2), 5 (0.1)  ~ 2K/u.
FINAL BRACKETS [best lower, best upper(DP L=3)], u=1, per site:
 p=0.4: h [0.03403, 0.03736]  a [0.11682, 0.12970]  E [0.16913, 0.16917]
 p=0.3: h [0.04012, 0.04902]  a [0.12644, 0.15401]  E [0.23240, 0.23285]
 p=0.2: h [0.04460, 0.06197]  a [0.12980, 0.17747]  E [0.31077, 0.31376]
 p=0.1: h [0.04438, 0.07542]  a [0.11663, 0.19678]  E [0.40172, 0.41799]
 cube:  0.029139 / 0.110944 / 0.120115.   All 12 lower bounds exceed the cube: the interaction RAISES all three exponents at u=1.

## Validations (code/y08_validate.py, out/y08_validate.txt, 12 s)
 (a) DP inequality, 300 random cases (inhomogeneous binary chains n=5..8, random members incl. cones/anti-cones, random Markov Q, t in (.1,.9)):
     min ratio lhs/rhs = 1.129 >= 1.
 (b) F+ sub-additive (F+_2-2F+_1 = -0.04..-0.11, F+_3-F+_1-F+_2 = -0.04..-0.12), F- super-additive (+0.02..+0.035), F- <= F <= F+,
     (F+_3-F-_3)/(t*2(u+K)) <= 0.096, DP block function sub-additive: all as proved.
 (c) Step 5: class-wise upper quantiles: type classes of the cube: 0 violations in 600; Markov (pair) type classes (n=9, 74 classes):
     598 violations in 600 (largest excess 6.0 = 6 flips); explicit example psi = d(., 000000010), x=110000000, y=010000000 violated.
 (d) exact increments of ln E[Xi^r] converge geometrically (ratios 0.88, 0.56) to the transfer-operator value: operator confirmed.

## Scans (code/y09_slopes_and_strong_coupling.py, out/y09_slopes_strong.txt, 77 s)
 (1) p=0.3, slope dependence, h: Lyapunov lower bound / cube = 2.27 (u=.05), 2.21 (.1), 2.02 (.25), 1.74 (.5), 1.33 (1), 0.994 (2), 0.925 (3), 0.928 (4);
     DP(L=1) upper / cube = 2.33, 2.33, 2.29, 2.17, 1.88, 1.46, 1.26, 1.16.  => small slopes: factor -> chi=(1-p)/p=2.333 (bracket [2.27,2.33] at u=.05),
     as predicted; for u>=2 the lower bound is BELOW the cube: direction for h undecided at large slopes.  E_F/E_cube: 2.33 .. 1.24 (always >1).
 (2) u=1, p->0: E_F -> u/2 (0.499 at p=.001).  DP(L=1) upper bounds saturate (h<=0.116, a<=0.302) and the Markov lower bound for h falls below
     the cube at p=.02 (0.0274): NOTHING is decided for p<=0.05.  My note (vii) "cost exponents -> 0 like p" was WRONG in rate: label domains of
     length ~2K/u still steer the chain, so the decay can only be like u/K = u/ln(1/p) [heuristic]; no bound of mine shows a decrease at any p>=.001.

## Tilt-state recursion "DP2" (code/ydp2.py, y10_dp2.py, y11_dp2_bounds.py; out/y10_dp2_parts12.txt, out/y11_dp2_p0.3.txt)
Idea: sum_x pi_phi^t Q^(1-t) = sum over paths of prod_i tau_{lam_i(x_<i)}(x_{i-1},x_i)^t q(x_{i-1},x_i)^(1-t) where lam_i = tilt of the conditional
law of pi_phi; every phi in C gives a tilt process with: exists theta_+-(prefix) in [-u,u]: mu_+ = mu_- + theta_+ - theta_-,
lam = ln[(1-p)e^{theta_+ + mu_-} + p e^{theta_-}] - ln[p e^{mu_-} + 1-p], |lam_n| <= u.  Minimising over all such processes = DP in (prev letter, tilt).
- TEST (n=3,4; all vertices; p=.4,.3,.1; t=.3,.45,.7; two Markov Q each): relaxed value == exact max over all vertices of (1-t)D_t(pi_phi||Q)
  to 6 digits in all 36 cases; relaxed max of KL(pi||pi_phi) == exact to 7 digits (6 cases).  The relaxation is TIGHT there.
- THRESHOLD: stationary relaxed growth of max KL(pi||pi_phi) = 0.1691273, 0.2324005, 0.3107665, 0.4017194 for p=.4,.3,.2,.1
  = E_F to <= 1e-9, independent of the grid (G=201..801, C=21..41).  => E_inf <= E_F numerically; with E_inf >= E_F [proved]:
  E_inf = E_F = ln[(1-p)cosh(u/2) + sqrt((1-p)^2 sinh^2(u/2) + p^2)]  [proved bound + numerical evaluation of a proved relaxation].
- With Q = pi the worst label is the uniform field and the rate is t E_F(u) - E_F(t u) (0.048861 at p=.3, t=.43; grid-independent to 1e-9).
- With a more ferromagnetic Markov centre (qt ~ 0.24 at p=0.3) the bound drops: F_inf(t) <= 0.04207 (t=.35), 0.04288 (.40), 0.04282 (.45), 0.04197 (.50)
  on the grid G=201,C=21  => h <~ 0.0430 at p=0.3 (lower bound 0.0401).
- OWN ERRORS here: (1) first finite-n version interpolated across the boundary of the feasible tilt interval (fixed: level-dependent grids);
  (2) part 3 of y10 was far too slow (440 rates) and printed nothing before the 10-min limit; (3) a damped iteration destroyed the monotone
  bracket (min(TW/W) nondecreasing only for the plain iteration) and gave grid-dependent "safe ends"; reverted;
  (4) a coarse control grid (G=101,C=11) gives SMALLER values (0.04218 instead of 0.04288 at t=.40): the control discretisation errs on the
  UNSAFE side; a grid-convergence study (y12) is running; until it converges the DP2 numbers for h, a are [numerical, not certified].

## Tilt-state recursion, conservative discretisation "DP3" (code/ydp3.py, y12_dp2_grid.py, y13_certified_upper.py, y15_dp3_controls.py)
- y12 (grid study of the theta-grid version, p=0.3,t=0.40,qt=0.2413): the "safe end" GROWS with the control resolution
  (0.04288 at C=11,21; 0.0446 at C=41; 0.0451 at C=81): the earlier value 0.0429 was an artefact of a coarse control grid.  [own error, caught by the study]
- New scheme: children's tilts on the tilt grid; feasible region enlarged by 1.5*spacing and stage factors minimal over the cell => grid value
  is on the SAFE side by induction (proof in the report); range-minimum queries make a sweep O(G^2).  Controls (y15): p=1/2 returns the cube exactly
  in the grid-restricted mode (0.0291391, 0.1201145, 0.1109441) and from above in the safe mode (G=3201: 0.0292072, 0.1201867, 0.1110063);
  n=4 exact maxima over all vertices <= 4*safe rate in 18 cases; p=0.3,t=0.43,qt=0.255: safe 0.04639/0.04547/0.04494/0.04468 (G=201..1601)
  decreasing, grid-restricted 0.04400/0.04417/0.04429/0.04435 increasing => relaxed rate in [0.04435, 0.04468].
- Results (y13, G=801; out/y13_upper_p*.txt): upper bounds over ALL t by the interval rule (F/t nonincr., F/(1-t) nondecr.):
    p=0.4: h <= 0.036163, a <= 0.121446;  p=0.3: h <= 0.044995, a <= 0.140860;  p=0.2: h <= 0.054353, a <= 0.160745;  p=0.1: h <= 0.066765, a <= 0.192774.
- THRESHOLD: relaxed growth of max KL(pi||pi_phi): grid-restricted value = E_F to 7 digits for p=0.4,0.3,0.2; safe value - E_F = 1.0e-4, 1.4e-4, 1.9e-4 at G=3201
  (halves with the spacing).  => E_inf = E_F for p=0.4,0.3,0.2 up to these certified margins.
  p=0.1: grid-restricted value 0.42389 > E_F = 0.40172: the relaxation is NOT tight there (or E_n > ln z_n for long chains).  My note above
  ("= E_F for p=.1" from the theta-grid version) was WRONG: the coarse control grid had hidden the better relaxed strategy.  [own error]
  Test (y14, 43 s): successive linearisation (LP ascent) of J(phi)=KL(pi||pi_phi) on n=8,10,12, p=.3,.2,.1,.05, 8-12 starts each: no phi in C with
  J > ln z_n found; the uniform field is the best local maximum in all 12 cases.  So for p=0.1: E in [0.40172, 0.41799] (upper: DP L=3), exactness of E_F open.
FINAL BRACKETS (per site, u=1; lower: Lyapunov/block-label; upper: tilt-state safe G=801, E: best of tilt-state G=3201 and DP L=3):
 p=0.4: h [0.034026, 0.036163]  a [0.116817, 0.121446]  E [0.169127, 0.169165]
 p=0.3: h [0.040115, 0.044995]  a [0.126444, 0.140860]  E [0.232400, 0.232538]
 p=0.2: h [0.044599, 0.054353]  a [0.129797, 0.160745]  E [0.310766, 0.310956]
 p=0.1: h [0.044378, 0.066765]  a [0.116632, 0.192774]  E [0.401719, 0.417991]

## Wrap-up
- y16 (16 s): headline lower bounds re-evaluated independently: G_L from M_L without a solver; Lam_blk by the operator with N=40, 80 and by exact
  increments of ln E[c^t] over k=1,2,3 blocks: agreement 1e-7..1e-5; bounds 0.040115 (p=.3), 0.034026 (.4), 0.044599 (.2), 0.044378 (.1) confirmed.
- y15 (256 s): controls of the conservative recursion pass (cube exact / from above; n=4 exact maxima below 4*safe rate; two-sided grid convergence).
- y10 part 1 re-run with the final code (4 s): unchanged.  Caveat written into the report: that tightness test only covers qt >= p.
- A transcription error of mine in the draft report (two rows of the (L') table for p=0.2, 0.1 written from memory, not from the output) was caught
  by checking every table entry against the out files; corrected (p=0.2: 0.00329, 0.01031, 0.01742; p=0.1: L=1 not available, 0.00327, 0.01020).
- Report: Y_report.md (final).  Scripts: code/y00..y16, libraries ylib.py, ylyap.py, ydp2.py, ydp3.py.  Outputs: out/.
