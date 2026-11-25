# Workstream X — working notes (updated after every step)

Question: is a worst-case (set-membership) envelope class the right representation of what is
not known about a molecular energy residual; if not, what replaces it and with which guarantees.

Labels: [V] machine-checked, [P] paper proof here, [K] known+cited (reading level), [N] numerics
only, [C] conjecture, [H] heuristic.

## Log

### 2026-11-25 17:41 UTC — start
* Read COMMON.md, X_brief.md, README.md (theory status, items (i)-(x)).
* Created this directory.  Nothing else written yet.
* Next: THEORY_REPORT §10 table, §11.2–11.4, 11.7, 11.12, 11.14, 11.17, §12; DEAD_ENDS D28, D32,
  D40, D42; docs/workstreams/README.md.

### 17:55 — reading done; plan
Read: THEORY_REPORT §10 (G1–G27 + the table "what each kind of knowledge costs" + three readings),
§11.1–11.5, §11.7, §11.10 (Thm 11.22/11.23), §11.12–11.14, §11.17, §12; DEAD_ENDS D28, D32, D40–D42;
docs/workstreams/README.md.  Sibling science briefs: A1/A2 (prior art of their clusters), K, M, P
(physical applicability of envelope classes), R1, R2 — P is the nearest neighbour; I do not duplicate
its question (do real residuals lie in the classes) but ask which *kind* of class/model.

Key observations while reading (to be tested numerically before any proof):
* O1.  Brief's product covariance k = s^2 rho^{d_H} on {0,1}^n has Walsh eigenvalues
  s^2 a^{n-|S|} b^{|S|}, a=(1+rho)/2, b=(1-rho)/2: the variance carried by interaction order m is
  Binomial(n,(1-rho)/2).  Fixed rho<1 => typical order is extensive.  Bounded order needs
  rho = 1-2*lam/n (Poisson(lam) orders).  IBC "product weights" gamma_i <-> rho_i=(1-gamma_i)/(1+gamma_i).
* O2.  GP credible band = z_delta * P_A(x); RKHS-ball worst-case band = B * P_A(x), same power
  function P_A.  So "Bayes vs worst case" is NOT the operative distinction; "ellipsoid (linear
  information) vs Lipschitz polytope (tropical information)" is.  Theory division's box-linear class is
  the l^infty sibling (l^1 span distance instead of power function).
* O3.  For linear designs A = C^perp (C a binary linear code) the posterior is explicit coset by
  coset (aliasing): P_A(x)^2 = sum_cosets 4pq/(p+q) <= 4 * (non-leader spectral mass).  With dual
  BCH codes: N <= (n+1)^m points give sup_x P_A^2 <= 4 tau_m^2 (tau_m^2 = variance beyond order m).
  Lower bound for ANY N points: avg_x P_A^2 >= sum of all but the N largest eigenvalues.
* O4.  Deterministic lower bound for min at the zero instance over the ball: error >= (B/2) max_x P_A(x).
* O5.  ln Z over a ball: exact consistent interval by Gibbs variational principle + Sion:
  U_A = sup_pi [beta B_A sqrt(pi^T K_A pi) - KL(pi||pi_hat)], L_A = inf_pi [beta B_A sqrt(..) + KL].
* O6.  Bayesian: dimension-free credible interval for ln Z from Jensen + annealed bound + Gaussian
  concentration (no union bound); min needs sqrt(2 ln|X|) (REM-like tails) — but value problems
  self-average: REM tail shows "polynomial iff spectrum decays" is FALSE for the VALUE of ln Z at
  high temperature in the Bayesian setting (prior alone predicts it).  To test.
* O7.  "No free hedging": Thm 11.22/11.23 are instance-wise, so an algorithm that is cheap on a nice
  subclass cannot be correct on the first-order class — the alternative assumption cannot be verified
  with polynomially many evaluations.
* O8.  Direction 3: sharpness certificate = MAP of f - c d_H(x*,.) (unary modification).  LP tight for
  trees and binary submodular (closed under unary changes).  Define LP-funnel slope c_LP <= tau.

Plan of numerics (each before the corresponding proof):
 N1 coset formula for P_A vs direct GP posterior;  N2 eigenvalue-tail lower bound;
 N3 ball certificate + ln Z variational interval vs brute force;  N4 Bayesian coverage;
 N5 same toy problem, cost vs n: first-order envelope (covering) vs ball vs GP;
 N6 misspecification: wrong spectrum, dips, conformal recalibration;
 N7 exponent for product covariance, fixed rho vs rho=1-2lam/n;  N8 REM tail (refutation of "iff");
 N9 LP-funnel slope vs integer funnel slope on random pairwise instances.

### 18:20 — N1/N2 done (n1_coset_formula.py -> n1_coset_formula.json)
* cube.py: FWHT, spectra (isotropic, product), linear designs (span, syndromes), BCH parity checks,
  dense posterior, coset ("aliasing") posterior.
* [N] 300 random (spectrum, linear design) pairs, n=3..8: coset posterior == dense posterior
  (max rel. diff 2e-7, all in the heavy-tailed kind: pinv truncation); structural check independent
  of conditioning (K_A vanishes on A; K-K_A in span K(.,a)) to 2.7e-14.  => formula CONFIRMED.
* [N] sup_x Var <= 4*NL in all trials; largest observed sup/NL = 3.82 (so 4 is essentially sharp).
* [N] avg_x Var >= eigenvalue tail T(N) in all trials (min ratio 1.05).
* [N] BCH designs (n,m) = (7,1),(6,1),(5,1),(15,1),(15,2),(12,2),(10,2),(7,2),(15,3): min distance
  >= 2m+1 verified by brute force; N = 8,8,8,16,256,256,256,64,1024; NL <= tau_m^2 and
  sup Var <= 4 tau_m^2 (observed sup/tau^2 about 1.4-2.0).  Exact order-m priors: Var == 0.
* Decision: Theorem A = two-sided tractability statement for min over Walsh-ellipsoids
  (deterministic), Theorem B = exact consistent interval of ln Z over a ball (variational),
  Theorem C = Bayesian twin (credible intervals, variance sandwich, second-moment certificate),
  Corollary = no free hedging, Theorem D = LP-funnel slope (direction 3).

### 18:45 — N7 done (n7_exponent.py -> n7_exponent.json); N5 running; N3 running (slow under load ~17)
* [N] product covariance sigma^2 rho^{d_H}, fixed rho: two-sided bounds of Theorem A give
  (1/n) ln n_p -> h((1-rho)/2): rho=0.5: [0.567, 0.582] at n=2000 (h=0.5623); rho=0.9: [0.206,
  0.225] (h=0.1985); rho=0.99: [0.035, 0.047] (h=0.0315).  Convergence from above, O(n^{-1/2}).
* [N] rho = 1 - 2 lam/n: polynomial; degree between ~0.9 and ~2.4 (lam=.5, theta=.5) up to ~5-7
  (lam=2, theta=.1): the degree is the Poisson(lam) quantile at the tolerance, as predicted.
* [N] random linear designs (2000 trials each, n=10,12; 300 at n=14): mean non-leader mass
  below the expectation bound sum_U v_U min(1, rank(U)/N0) in all 12 cases (e.g. 0.0355 vs 0.0409),
  and sup_x Var <= 4 NL in all examples.  First attempt with 20 trials "failed" by Monte Carlo
  noise (NL is heavy-tailed: rare codes alias a main effect with the constant) — not a
  counterexample; kept in the log as a warning about small trial counts.
* N5 quick look (order-2 residual, eps=0.25): with oracle-tight envelope constants (kappa=1) and
  e/c ~ 1/2 the FIRST-ORDER paradigm is as cheap as the kernel one up to n=10 (greedy 34 vs 34);
  with a safety factor 2 on the constants (kappa=1/2) it is 186 vs 55 at n=10.  The envelope
  exponent is small (R*(1/2)=0.188/site): separation is asymptotic, not dramatic at toy sizes.
  => must report honestly; added Part II (additive toy, rigorous product lower bound, n to 1000).

### 19:05 — N3 done (n3_ball_lnz.py -> n3_ball_lnz.json, .log)
* LESSON (machine): load average 17 on 4 cores; numpy with multi-threaded BLAS stalls on small
  matrices.  ALWAYS run with OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1.  (First two N3 attempts timed
  out for this reason only.)
* [N] 60 random (kernel, design, f, beta, ball member) instances, |X| = 8..32:
  hypercircle band |g-ghat| <= B_A P_A: 0 violations; exact lower end of min attained (1.8e-15);
  U_A (search in function space) == sup_pi[beta B_A sqrt(pi K_A pi) - KL] and
  L_A == inf_pi[beta B_A sqrt(pi K_A pi) + KL] to 2e-7 / 7e-7 relative; ordering
  L_A <= beta B_A sqrt(pihat K_A pihat) <= U_A <= beta B_A max P_A: 0 violations.
* Wrinkle: in a first run 1/60 instances disagreed (1.97 vs 3.13).  Cause: the sup problem is a
  difference-of-convex maximisation with TWO kinds of local maxima — a delocalised perturbation
  and a localised (dip-like) one; random starts found only the first.  With localised starts both
  searches agree.  This is the ellipsoid's analogue of the dip: at large beta*B the worst member
  for ln Z localises.  (Worth one sentence in the report.)

### 19:25 — literature search log (queries, what was read, reading level)
Tool: web search (results = titles+snippets), page fetch for 3 URLs.  Levels: [abs] abstract read,
[snip] search snippet only, [mem] from memory — unverified.
 1. "Mitchell Morris Ylvisaker Two-level fractional factorials and Bayesian prediction" ->
    Statistica Sinica 5(2) (1995) 559-573 [abs, fetched stat.sinica.edu.tw; full text behind
    password].  Stationary GP prior on {-1,1}^k, conditioning on a fractional factorial,
    "useful regularities".  => the coset/aliasing posterior (my Lemma A1) is KNOWN in substance.
    Later: Kerr 2001, Joseph 2006 (Bayesian fractional factorial design) [snip].
 2. "Wasilkowski Woźniakowski Finite-order weights imply tractability of linear multivariate
    problems" -> J. Approx. Theory 130 (2004) 57-77, doi 10.1016/j.jat.2004.06.011 [snip/abs].
 3. "Kuo Sloan Woźniakowski Lattice rules for multivariate approximation in the worst case
    setting" -> MCQMC 2004 (Springer 2006) 289-330 [snip].  Lattice algorithm = aliasing over the
    dual lattice; my linear designs are its F_2 analogue (digital nets / Walsh).
 4. "Novak global optimization as hard as approximation" -> D. Krieg, PhD thesis arXiv:1905.01166
    [snip]: "global optimization is never harder than uniform approximation ... practically as
    hard ... if F is convex and symmetric [Was84, Nov88]".  => my lower bound for min over the ball
    is an instance of Wasilkowski 1984 / Novak 1988 [mem for the originals].
    Wasilkowski, "On average complexity of global optimization problems", Math. Programming 57
    (1992) 313-324 [abs]: optimisation is easier on average than in the worst case; only upper
    bounds; average complexity open.
 5. "Bayesian optimization combinatorial binary hypercube ... BOCS COMBO" -> Baptista-Poloczek
    2018 (BOCS, second-order model on binary variables), Oh et al. 2019 (COMBO, diffusion kernel
    on the graph Cartesian product = product kernel), Dadkhahi et al. 2020 (arXiv 2006.03963),
    Deshwal et al. [snip].  No regret/complexity theorem for Walsh-spectrum kernels with a
    matching lower bound surfaced in this search (absence of a match is NOT a novelty claim).
 6. "Bogunovic Krause Misspecified Gaussian process bandit optimization" -> NeurIPS 2021,
    arXiv:2111.05008 [abs]: true function eps-close in sup norm to an RKHS-ball member; EC-GP-UCB;
    regret bounds in eps, horizon, kernel.
 7. "Weller Rowland Sontag Tightness of LP relaxations for almost balanced models" -> AISTATS 2016
    (PMLR 51) [snip]: LP+LOC tight for balanced binary pairwise models; triplet relaxation tight
    iff blocks almost balanced.  Thapper-Zivny not surfaced [mem].
 8. "Lang Sontag Vijayaraghavan stable instances" -> AISTATS 2018 (arXiv:1711.02195) [abs,
    fetched]: ferromagnetic Potts, alpha-expansion and an LP relaxation recover the MAP under
    stability conditions; Block stability (arXiv:1810.05305) [snip]; Lang-Reddy-Sontag-
    Vijayaraghavan "Beyond perturbation stability" [snip].
 9. "Thomas Chen Ortner Body-ordered approximations of atomic properties" -> Arch. Ration. Mech.
    Anal. 246 (2022) 1-60, arXiv:2106.12572 [snip]: LDOS of tight-binding models has a weak
    body-order expansion; rates in terms of Fermi temperature and band gap.
10. "Bayesian quadrature log partition function" -> Rasmussen-Ghahramani "Bayesian Monte Carlo"
    (NIPS 2002/2003), Osborne et al. NIPS 2012, Gunter et al. 2014 WSABI (arXiv:1411.0439) [snip].
11. "Hinrichs Novak Ullrich Woźniakowski curse of dimensionality smooth functions" -> Math. Comp.
    83 (2014) 2853-2863, arXiv:1211.0871 [abs/snip]: curse for unit balls of C^r, also when
    directional derivatives are bounded by ~1/sqrt(d); part II J. Complexity 30 (2014) 117-143.
12. "Kanagawa Hennig Sejdinovic Sriperumbudur" -> arXiv:1807.02582 [snip]: sect. 3.4 "posterior
    variance = worst-case error in the RKHS unit ball".
13. Srinivas-Krause-Kakade-Seeger ICML 2010 / IEEE TIT 2012 (GP-UCB; GP sample or low RKHS norm;
    regret via maximal information gain) [snip]; Bull, JMLR 12 (2011) 2879-2904 [snip];
    Kandasamy-Schneider-Poczos ICML 2015 (additive models: regret linear in D) [snip].
14. Sloan-Woźniakowski, J. Complexity 14 (1998) 1-33 [snip]; Novak-Woźniakowski, Tractability of
    Multivariate Problems I-III (EMS 2008/2010/2012) [snip, titles only].

### 20:10 — N4/N8, N6, N9, N10 done; N5 part I done, part II running
* N5 part I (order-2 residual, eps=.25, medians of 5; n5_compare.log):
  sharp regime (e=2, kappa=1): W = 1 evaluation, H/B ~ n+1  -> the envelope paradigm WINS when the
  known part is sharp.  Non-sharp, oracle-tight constants (kappa=1, e=0): W best-first 19..336
  (n=6..12, x1.6/site), H 15..57, B 20..70.  Safety factor 2 (kappa=.5, e=0): W greedy 40..567
  (n=6..11), best-first 45..1423 (n=6..12, x1.78/site), H = M = 21..79, B 20..70.
  All H/B runs valid (true min inside [LB,UB]) in 5/5 everywhere.
* N5 part II, kappa=1: product lower bound = 0 for all n.  NOT a bug: with oracle-tight constants
  and an additive residual the envelope is saturated between argmax g and argmin g, two
  evaluations pin g on every geodesic = everywhere.  (Theory report notes kappa<1 is needed.)
  kappa=0.5 rows are the meaningful ones.
* N4 (n4_bayes.json): analytic (sup-norm) Bayesian intervals always cover, but for ln Z they are
  9-80x wider than the sampled posterior interval (n=15, m=2: 0.81 vs 0.010 at beta=.5; 3.33 vs
  0.37 at beta=2); for min only ~1.8x (1.30 vs 0.72).  => ln Z is governed by the Gibbs-averaged
  posterior covariance, not by sup P.  Sampled coverage 0.91-0.98 (nominal .95; 200 posterior
  samples shared across draws -> correlated MC error).  Cosmetic bug: rows with exact posterior
  (n=7, m=2: the "m=2" BCH code of length 7 is the repetition code, strength 6) show coverage
  0.73 at width 0 = float rounding in the coverage test.  FIX + rerun at the end.
* N8 (white tail tw2=1 unlearnable, main effects learnable): second-moment certificate width
  0.16 (n=12, N=256, beta=.5; true posterior 95% spread 0.07; sup-norm width 2.9), 0.61 at beta=1
  (true 0.28), vacuous at beta=2 (true spread 1.27), frozen at beta=4 (true spread 5.1).
* N6 (n6_misspec.json): nominal 95% interval for min: coverage .948 well specified; .557 pair
  variance x4; .770 unmodelled order 3; .930 t3 coefficients; dips at low states in 20% of
  instances: .795 overall = .089 on dipped / .957 on clean.  Split conformal restores marginal
  coverage in all cases (.953-.967) but only .767 on the dipped instances.  Goodness-of-fit on
  the same 16 evaluations rejects 76% (b), 29% (c), 8% of dipped (baseline 5.5%); 32 held-out
  evaluations reject 98% (b), 88% (c), 24% of dipped (baseline 11%).
  Lebesgue constants max_x sum_a |lambda_a(x)| = 2.5, 4.28, 2.875, 4.69, 3.25 for (n,m)=(7,1),(7,2),
  (10,1),(10,2),(12,1) (about 0.6-0.9 sqrt(M)); l2 norm of weights = sqrt(M/N) exactly.
* N9 (n9_lp_funnel.json): tau_LP <= tau in all 1360 instances (0 violations).  Ferromagnets
  (grid 4x4, chain12+6 contacts) and trees: tau_LP = tau in 100%.  Frustrated: grid weak field
  5-25% equal, LP tight at x* in 28-55%; strong field 80-85% equal, 93-100% tight; chain+contacts
  ~50% equal, 74-84% tight.  Triangle h=(-.5,0,-.5), J=(-1,-1,+1): tau=1/2, tau_LP=-2/3.
* N10 (n10_extras.json): (I) order-2 ellipsoid, f=0, B=sqrt(n), s2=.25: numerical sup of ln Z ==
  Curie-Weiss member to 4 digits at all (n,beta); O(1) below 2 beta b sqrt(s2)=1 (0.058 at .4),
  extensive above; sup-norm bound far above.  (II) RKHS norm of a depth-3 dip under the product
  spectrum with lam=.5: 3.9e3 (n=8) -> 1.7e9 (n=16) vs typical draw 16 -> 256 and an additive
  function of the same depth 3.3.
